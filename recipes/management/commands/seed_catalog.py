from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.catalog_data import PRODUCTS, RECIPES
from recipes.icon_generator import get_icon_svg
from recipes.product_photos import photo_name_for_slug
from recipes.models import LocalIngredient, LocalRecipe, RecipeIngredient


class Command(BaseCommand):
    help = 'Загружает каталог продуктов (с SVG-иконками) и полноценные рецепты'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Очистить продукты и рецепты перед загрузкой')
        parser.add_argument('--refresh-icons', action='store_true', help='Пересоздать все SVG-иконки продуктов')
        parser.add_argument('--cache-photos', action='store_true', help='Скачать фото продуктов после загрузки каталога')

    def handle(self, *args, **options):
        icons_dir = Path(settings.BASE_DIR) / 'static' / 'img' / 'products'
        icons_dir.mkdir(parents=True, exist_ok=True)

        if options['clear']:
            LocalRecipe.objects.all().delete()
            LocalIngredient.objects.all().delete()
            self.stdout.write(self.style.WARNING('Каталог очищен.'))

        product_count = 0
        for item in PRODUCTS:
            icon_name = f"{item['slug']}.svg"
            icon_path = icons_dir / icon_name
            if options['refresh_icons'] or not icon_path.exists():
                icon_path.write_text(get_icon_svg(item['slug']), encoding='utf-8')

            obj, created = LocalIngredient.objects.update_or_create(
                name=item['name'],
                defaults={
                    'slug': item['slug'],
                    'category': item['category'],
                    'sort_order': item['order'],
                    'icon_file': icon_name,
                    'photo_name': photo_name_for_slug(item['slug']),
                },
            )
            if created:
                product_count += 1

        recipe_count = 0
        for item in RECIPES:
            ingredients_text = ', '.join(item['ingredients'])
            recipe, created = LocalRecipe.objects.update_or_create(
                title=item['title'],
                defaults={
                    'instructions': item['instructions'].strip(),
                    'prep_time': item['prep_time'],
                    'servings': item.get('servings', 2),
                    'difficulty': item.get('difficulty', 'easy'),
                    'ingredients_text': ingredients_text,
                    'category': item['category'],
                    'card_emoji': item['card_emoji'],
                },
            )
            if created:
                recipe_count += 1

            RecipeIngredient.objects.filter(recipe=recipe).delete()
            for ing_name in item['ingredients']:
                ingredient = LocalIngredient.objects.filter(name=ing_name).first()
                if ingredient:
                    RecipeIngredient.objects.get_or_create(recipe=recipe, ingredient=ingredient)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: продуктов {LocalIngredient.objects.count()}, '
            f'рецептов {LocalRecipe.objects.count()} (+{recipe_count} новых).'
        ))

        if options['cache_photos']:
            from django.core.management import call_command
            call_command('cache_product_photos')
