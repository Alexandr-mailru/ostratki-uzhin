from django.db import models


class Ingredient(models.Model):
    """Устаревшая модель — оставлена для совместимости миграций."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Устаревшая модель — оставлена для совместимости миграций."""

    title = models.CharField(max_length=200)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LocalRecipe(models.Model):
    CATEGORY_CHOICES = [
        ('soup', 'Суп'),
        ('main', 'Основное'),
        ('salad', 'Салат'),
        ('breakfast', 'Завтрак'),
        ('dessert', 'Десерт'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Просто'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]

    title = models.CharField(max_length=300, verbose_name='Название')
    instructions = models.TextField(verbose_name='Инструкции')
    prep_time = models.IntegerField(null=True, blank=True, verbose_name='Время (мин)')
    servings = models.PositiveSmallIntegerField(default=2, verbose_name='Порций')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    ingredients_text = models.TextField(help_text='Для поиска по строке')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    card_emoji = models.CharField(max_length=8, default='🍽️', verbose_name='Эмодзи на карточке')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Локальный рецепт'
        verbose_name_plural = 'Локальные рецепты'

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        emoji = self.card_emoji or '🍽️'
        return f'https://placehold.co/400x240/e8f5e9/2e7d32?text={emoji}'

    @property
    def ingredients_list(self):
        return [i.strip() for i in self.ingredients_text.split(',') if i.strip()]

    @property
    def instruction_steps(self):
        steps = []
        for line in self.instructions.splitlines():
            text = line.strip()
            if not text:
                continue
            if len(text) > 2 and text[0].isdigit() and text[1] in '.).':
                text = text[2:].strip()
            elif len(text) > 3 and text[:2].isdigit() and text[2] in '.).':
                text = text[3:].strip()
            steps.append(text)
        return steps

    @property
    def difficulty_label(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty, '')


class LocalIngredient(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    category = models.CharField(max_length=50, default='Прочее')
    sort_order = models.PositiveIntegerField(default=0)
    icon_file = models.CharField(max_length=120, blank=True, help_text='Имя SVG в static/img/products/')
    photo_name = models.CharField(max_length=120, blank=True, help_text='Имя файла на CDN Spoonacular')
    photo_file = models.CharField(max_length=120, blank=True, help_text='Локальный кэш фото')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        from .product_photos import PHOTOS_STATIC_DIR, cdn_url, local_photo_path

        if self.photo_file:
            return f'/static/{PHOTOS_STATIC_DIR}/{self.photo_file}'
        if self.slug:
            cached = local_photo_path(self.slug)
            if cached:
                return cached
        if self.photo_name:
            return cdn_url(self.photo_name)
        if self.icon_file:
            return f'/static/img/products/{self.icon_file}'
        if self.slug:
            return f'/static/img/products/{self.slug}.svg'
        return '/static/img/products/default.svg'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(LocalRecipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(LocalIngredient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'ingredient')

