from django.core.management.base import BaseCommand

from recipes.models import LocalIngredient, LocalRecipe, RecipeIngredient

DEMO_RECIPES = [
    {
        'title': 'Яичница с помидорами',
        'category': 'breakfast',
        'card_emoji': '🍳',
        'prep_time': 15,
        'ingredients': ['яйца', 'помидоры', 'лук', 'соль', 'перец', 'подсолнечное масло'],
        'instructions': (
            '1. Нарежьте помидоры и лук.\n'
            '2. Обжарьте овощи на сковороде 3–4 минуты.\n'
            '3. Вбейте яйца, посолите и поперчите.\n'
            '4. Готовьте на среднем огне до желаемой степени прожарки.'
        ),
    },
    {
        'title': 'Картофельное пюре с сыром',
        'category': 'main',
        'card_emoji': '🥔',
        'prep_time': 35,
        'ingredients': ['картофель', 'молоко', 'сливочное масло', 'сыр', 'соль'],
        'instructions': (
            '1. Отварите картофель до мягкости.\n'
            '2. Разомните с молоком и маслом.\n'
            '3. Добавьте тертый сыр и перемешайте.\n'
            '4. Подавайте горячим.'
        ),
    },
    {
        'title': 'Куриный суп с лапшой',
        'category': 'soup',
        'card_emoji': '🍲',
        'prep_time': 50,
        'ingredients': ['курица', 'морковь', 'лук', 'картофель', 'лапша', 'соль', 'лавровый лист'],
        'instructions': (
            '1. Сварите бульон из курицы.\n'
            '2. Добавьте нарезанные овощи.\n'
            '3. Через 15 минут положите лапшу.\n'
            '4. Доведите до готовности и дайте настояться 5 минут.'
        ),
    },
    {
        'title': 'Гречка с яйцом и луком',
        'category': 'main',
        'card_emoji': '🌾',
        'prep_time': 25,
        'ingredients': ['гречка', 'яйца', 'лук', 'подсолнечное масло', 'соль'],
        'instructions': (
            '1. Отварите гречку в пропорции 1:2 с водой.\n'
            '2. Обжарьте лук до золотистого цвета.\n'
            '3. Сварите яйца вкрутую и нарежьте.\n'
            '4. Смешайте гречку с луком и яйцом.'
        ),
    },
    {
        'title': 'Салат «Остатки в холодильнике»',
        'category': 'salad',
        'card_emoji': '🥗',
        'prep_time': 10,
        'ingredients': ['огурцы', 'помидоры', 'сыр', 'оливковое масло', 'соль', 'перец'],
        'instructions': (
            '1. Нарежьте овощи кубиками.\n'
            '2. Добавьте сыр соломкой.\n'
            '3. Заправьте маслом, солью и перцем.\n'
            '4. Перемешайте и подавайте сразу.'
        ),
    },
    {
        'title': 'Овсянка с бананом и мёдом',
        'category': 'breakfast',
        'card_emoji': '🥣',
        'prep_time': 12,
        'ingredients': ['овсянка', 'молоко', 'бананы', 'мед'],
        'instructions': (
            '1. Сварите овсянку на молоке.\n'
            '2. Нарежьте банан.\n'
            '3. Добавьте мёд по вкусу.\n'
            '4. Подавайте тёплой.'
        ),
    },
    {
        'title': 'Рис с овощами',
        'category': 'main',
        'card_emoji': '🍚',
        'prep_time': 30,
        'ingredients': ['рис', 'морковь', 'перец сладкий', 'лук', 'подсолнечное масло', 'соль'],
        'instructions': (
            '1. Отварите рис до готовности.\n'
            '2. Обжарьте нарезанные овощи.\n'
            '3. Смешайте рис с овощами.\n'
            '4. Посолите и прогрейте 2 минуты.'
        ),
    },
    {
        'title': 'Творожные оладьи',
        'category': 'dessert',
        'card_emoji': '🥞',
        'prep_time': 20,
        'ingredients': ['яйца', 'мука', 'сахар', 'сметана', 'подсолнечное масло'],
        'instructions': (
            '1. Смешайте яйца, муку, сахар и сметану до однородности.\n'
            '2. Выложите ложкой на разогретую сковороду.\n'
            '3. Жарьте с двух сторон до румяности.\n'
            '4. Подавайте со сметаной или вареньем.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Загружает демо-рецепты на русском языке (без внешнего CSV)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить существующие локальные рецепты перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            LocalRecipe.objects.all().delete()
            self.stdout.write(self.style.WARNING('Локальные рецепты удалены.'))

        created = 0
        for item in DEMO_RECIPES:
            ingredients_text = ', '.join(item['ingredients'])
            recipe, was_created = LocalRecipe.objects.get_or_create(
                title=item['title'],
                defaults={
                    'instructions': item['instructions'],
                    'prep_time': item['prep_time'],
                    'ingredients_text': ingredients_text,
                    'category': item['category'],
                    'card_emoji': item['card_emoji'],
                },
            )
            if was_created:
                created += 1
                for ing_name in item['ingredients']:
                    ingredient, _ = LocalIngredient.objects.get_or_create(name=ing_name)
                    RecipeIngredient.objects.get_or_create(recipe=recipe, ingredient=ingredient)

        self.stdout.write(self.style.SUCCESS(f'Готово. Добавлено новых рецептов: {created}.'))
