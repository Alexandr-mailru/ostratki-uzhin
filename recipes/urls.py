from django.urls import path

from . import views

urlpatterns = [
    path('', views.recipe_search, name='recipe_search'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('copyright/', views.copyright_info, name='copyright_info'),
    path('clear/', views.clear_fridge, name='clear_fridge'),
    path('favorites/', views.favorites_page, name='favorites_page'),
    path('recipe/<slug:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<slug:recipe_id>/pdf/', views.recipe_pdf, name='recipe_pdf'),
    path('favorite/<slug:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
]
