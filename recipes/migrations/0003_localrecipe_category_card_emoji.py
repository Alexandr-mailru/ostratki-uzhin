from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_localingredient_localrecipe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='localrecipe',
            name='card_emoji',
            field=models.CharField(default='🍽️', max_length=8, verbose_name='Эмодзи на карточке'),
        ),
        migrations.AddField(
            model_name='localrecipe',
            name='category',
            field=models.CharField(
                choices=[
                    ('soup', 'Суп'),
                    ('main', 'Основное'),
                    ('salad', 'Салат'),
                    ('breakfast', 'Завтрак'),
                    ('dessert', 'Десерт'),
                ],
                default='main',
                max_length=20,
            ),
        ),
    ]
