from django.contrib import admin

from .models import LocalIngredient, LocalRecipe, RecipeIngredient


@admin.register(LocalRecipe)
class LocalRecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'prep_time', 'servings', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'ingredients_text')


@admin.register(LocalIngredient)
class LocalIngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'sort_order')
    list_filter = ('category',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')
