from django import forms

TIME_CHOICES = [
    ('', 'Любое время'),
    ('15', 'До 15 минут'),
    ('30', 'До 30 минут'),
    ('60', 'До 1 часа'),
    ('120', 'До 2 часов'),
]


class IngredientForm(forms.Form):
    ingredients = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'ingredients-input'}),
        required=False,
    )
    max_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        required=False,
        label='Время готовки',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )
