import json

import requests
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from xhtml2pdf import pisa

from collections import OrderedDict

from .forms import IngredientForm
from .models import LocalIngredient, LocalRecipe
from .product_photos import photo_url_for_slug
from .translations import translate_ingredients

SITE_NAME = 'Остатки → Ужин'


def get_product_categories():
    categories = OrderedDict()
    products = LocalIngredient.objects.exclude(slug='').order_by('sort_order', 'name')
    if not products.exists():
        from .catalog_data import PRODUCTS
        for item in PRODUCTS:
            categories.setdefault(item['category'], []).append({
                'name': item['name'],
                'icon_url': photo_url_for_slug(item['slug']),
            })
        return categories

    for product in products:
        categories.setdefault(product.category, []).append({
            'name': product.name,
            'icon_url': product.icon_url,
        })
    return categories


def _normalize_favorite_id(recipe_id):
    return str(recipe_id)


def _session_favorites(request):
    return [_normalize_favorite_id(fid) for fid in request.session.get('favorites', [])]


def find_local_recipes(ingredient_list):
    if not ingredient_list:
        return []

    scored = []
    for recipe in LocalRecipe.objects.prefetch_related('recipe_ingredients__ingredient'):
        recipe_names = {
            ri.ingredient.name.lower()
            for ri in recipe.recipe_ingredients.all()
        }
        recipe_names.update(i.strip().lower() for i in recipe.ingredients_text.split(',') if i.strip())

        matched = 0
        for selected in ingredient_list:
            if selected in recipe_names or any(selected in n or n in selected for n in recipe_names):
                matched += 1

        if matched == 0:
            continue

        total = max(len(recipe.ingredients_list), len(recipe_names))
        missed = max(0, total - matched)
        scored.append((matched, missed, recipe))

    scored.sort(key=lambda row: (-row[0], row[1], row[2].prep_time or 999))

    results = []
    for matched, missed, recipe in scored[:50]:
        total = matched + missed
        match_percent = round((matched / total) * 100) if total else 0
        results.append({
            'id': f'local_{recipe.id}',
            'title': recipe.title,
            'image': recipe.image_url,
            'usedIngredientCount': matched,
            'missedIngredientCount': missed,
            'totalIngredients': total,
            'matchPercent': match_percent,
            'readyInMinutes': recipe.prep_time or 45,
            'is_local': True,
            'difficulty': recipe.difficulty,
            'difficulty_label': recipe.difficulty_label,
            'category': recipe.category,
        })
    return results


def recipe_search(request):
    results = []
    ingredients_display = []
    saved_fridge = request.session.get('fridge_ingredients', '')
    api_configured = bool(settings.SPOONACULAR_API_KEY)

    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            raw_input = form.cleaned_data['ingredients']
            request.session['fridge_ingredients'] = raw_input

            if ',' in raw_input:
                ingredient_list = [x.strip().lower() for x in raw_input.split(',') if x.strip()]
            else:
                ingredient_list = [x.strip().lower() for x in raw_input.split('\n') if x.strip()]

            ingredients_display = ingredient_list
            local_results = find_local_recipes(ingredient_list)

            api_results = []
            if api_configured and ingredient_list:
                translated_ingredients = translate_ingredients(ingredient_list)
                ingredients_str = ','.join(translated_ingredients)
                url = 'https://api.spoonacular.com/recipes/findByIngredients'
                params = {
                    'ingredients': ingredients_str,
                    'number': 50,
                    'ranking': 1,
                    'ignorePantry': True,
                    'apiKey': settings.SPOONACULAR_API_KEY,
                }
                try:
                    response = requests.get(url, params=params, timeout=12)
                    if response.status_code == 200:
                        api_results = response.json()
                        if form.cleaned_data.get('max_time'):
                            max_time = int(form.cleaned_data['max_time'])
                            api_results = [
                                r for r in api_results
                                if r.get('readyInMinutes', 999) <= max_time
                            ]
                        for recipe in api_results:
                            used = recipe.get('usedIngredientCount', 0)
                            missed = recipe.get('missedIngredientCount', 0)
                            total = used + missed
                            recipe['totalIngredients'] = total
                            recipe['matchPercent'] = round((used / total) * 100) if total else 0
                            recipe['is_local'] = False
                            recipe['id'] = str(recipe.get('id'))
                except requests.RequestException:
                    pass

            results = local_results + api_results
            results.sort(key=lambda r: (r.get('missedIngredientCount', 999), r.get('readyInMinutes', 999)))
    else:
        form = IngredientForm(initial={'ingredients': saved_fridge}) if saved_fridge else IngredientForm()

    favorites = _session_favorites(request)
    return render(request, 'recipes/search.html', {
        'form': form,
        'results': results,
        'results_json': json.dumps(results, ensure_ascii=False),
        'favorites_json': json.dumps(favorites, ensure_ascii=False),
        'ingredients_display': ingredients_display,
        'ingredient_categories': get_product_categories(),
        'api_configured': api_configured,
        'show_api_hint': settings.DEBUG and not api_configured,
        'site_name': SITE_NAME,
    })


def recipe_detail(request, recipe_id):
    recipe_id = _normalize_favorite_id(recipe_id)
    favorites = _session_favorites(request)

    if recipe_id.startswith('local_'):
        local_id = recipe_id.replace('local_', '')
        recipe = get_object_or_404(LocalRecipe, id=local_id)
        return render(request, 'recipes/local_detail.html', {
            'recipe': recipe,
            'recipe_id': recipe_id,
            'is_favorite': recipe_id in favorites,
            'site_name': SITE_NAME,
        })

    if not settings.SPOONACULAR_API_KEY:
        return render(request, 'recipes/detail.html', {'recipe': None, 'site_name': SITE_NAME})

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {'apiKey': settings.SPOONACULAR_API_KEY, 'language': 'ru', 'includeNutrition': False}
    recipe = None
    try:
        response = requests.get(url, params=params, timeout=12)
        if response.status_code == 200:
            recipe = response.json()
            recipe['id'] = str(recipe.get('id'))
    except requests.RequestException:
        recipe = None

    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        'recipe_id': recipe_id,
        'is_favorite': recipe_id in favorites,
        'site_name': SITE_NAME,
    })


def recipe_pdf(request, recipe_id):
    recipe_id = _normalize_favorite_id(recipe_id)

    if recipe_id.startswith('local_'):
        local_id = recipe_id.replace('local_', '')
        recipe_obj = get_object_or_404(LocalRecipe, id=local_id)
        recipe = {
            'title': recipe_obj.title,
            'readyInMinutes': recipe_obj.prep_time,
            'extendedIngredients': [{'original': ing} for ing in recipe_obj.ingredients_list],
            'instructions': recipe_obj.instructions.replace('\n', '<br>'),
        }
        html = render_to_string('recipes/recipe_pdf.html', {'recipe': recipe, 'site_name': SITE_NAME})
    else:
        if not settings.SPOONACULAR_API_KEY:
            return HttpResponse('API не настроен', status=503)
        try:
            response = requests.get(
                f'https://api.spoonacular.com/recipes/{recipe_id}/information',
                params={'apiKey': settings.SPOONACULAR_API_KEY, 'language': 'ru'},
                timeout=12,
            )
            recipe = response.json() if response.status_code == 200 else None
            if not recipe:
                return HttpResponse('Рецепт не найден', status=404)
            html = render_to_string('recipes/recipe_pdf.html', {'recipe': recipe, 'site_name': SITE_NAME})
        except requests.RequestException:
            return HttpResponse('Ошибка загрузки рецепта', status=500)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="recipe_{recipe_id}.pdf"'
        return response
    return HttpResponse('Ошибка генерации PDF', status=500)


def clear_fridge(request):
    request.session.pop('fridge_ingredients', None)
    return redirect('recipe_search')


@require_POST
def toggle_favorite(request, recipe_id):
    recipe_id = _normalize_favorite_id(recipe_id)
    favorites = _session_favorites(request)

    if recipe_id in favorites:
        favorites.remove(recipe_id)
        is_favorite = False
    else:
        favorites.append(recipe_id)
        is_favorite = True

    request.session['favorites'] = favorites
    return JsonResponse({'is_favorite': is_favorite, 'count': len(favorites)})


def favorites_page(request):
    favorites = _session_favorites(request)
    recipes = []
    api_key = settings.SPOONACULAR_API_KEY

    for rid in favorites:
        try:
            if rid.startswith('local_'):
                local_id = rid.replace('local_', '')
                local_recipe = LocalRecipe.objects.get(id=local_id)
                recipes.append({
                    'id': rid,
                    'title': local_recipe.title,
                    'image': local_recipe.image_url,
                    'is_local': True,
                })
            elif api_key:
                response = requests.get(
                    f'https://api.spoonacular.com/recipes/{rid}/information',
                    params={'apiKey': api_key, 'language': 'ru'},
                    timeout=8,
                )
                if response.status_code == 200:
                    data = response.json()
                    data['id'] = str(data.get('id'))
                    recipes.append(data)
        except (LocalRecipe.DoesNotExist, requests.RequestException):
            continue

    return render(request, 'recipes/favorites.html', {
        'recipes': recipes,
        'site_name': SITE_NAME,
    })


def about(request):
    return render(request, 'about.html', {'site_name': SITE_NAME})


def privacy(request):
    return render(request, 'privacy.html', {'site_name': SITE_NAME})


def copyright_info(request):
    return render(request, 'copyright.html', {'site_name': SITE_NAME})
