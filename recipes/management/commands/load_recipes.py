import csv
import ast
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import LocalRecipe, LocalIngredient, RecipeIngredient


class Command(BaseCommand):
    help = 'Загружает рецепты из RecipeNLG CSV в локальную БД'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к full_dataset.csv')

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {csv_path}'))
            return

        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Безопасный парсинг списков
                    ingredients = ast.literal_eval(row['ingredients'])
                    instructions = ast.literal_eval(row['directions'])
                    title = row['title'].strip()

                    if not title or not ingredients or not instructions:
                        continue

                    # Объединяем шаги в один текст
                    instructions_text = '\n'.join(instructions)
                    ingredients_text = ', '.join(ingredients).lower()

                    # Создаём рецепт
                    recipe = LocalRecipe.objects.create(
                        title=title,
                        instructions=instructions_text,
                        ingredients_text=ingredients_text,
                        prep_time=None  # RecipeNLG не содержит времени
                    )

                    # Создаём связи с ингредиентами
                    for ing_name in ingredients:
                        ing_clean = ing_name.strip().lower()
                        if not ing_clean:
                            continue
                        ingredient, _ = LocalIngredient.objects.get_or_create(name=ing_clean)
                        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

                    count += 1
                    if count % 1000 == 0:
                        self.stdout.write(f'Загружено: {count} рецептов...')

                except (ValueError, SyntaxError, KeyError) as e:
                    # Пропускаем битые строки
                    continue

        self.stdout.write(self.style.SUCCESS(f'Загрузка завершена! Всего: {count} рецептов.'))
