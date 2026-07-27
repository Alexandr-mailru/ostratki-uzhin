from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_localrecipe_category_card_emoji'),
    ]

    operations = [
        migrations.AddField(
            model_name='localingredient',
            name='category',
            field=models.CharField(default='Прочее', max_length=50),
        ),
        migrations.AddField(
            model_name='localingredient',
            name='icon_file',
            field=models.CharField(blank=True, help_text='Имя SVG в static/img/products/', max_length=120),
        ),
        migrations.AddField(
            model_name='localingredient',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='localingredient',
            name='sort_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='localrecipe',
            name='difficulty',
            field=models.CharField(
                choices=[('easy', 'Просто'), ('medium', 'Средне'), ('hard', 'Сложно')],
                default='easy',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='localrecipe',
            name='servings',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='Порций'),
        ),
        migrations.AlterModelOptions(
            name='localingredient',
            options={'ordering': ['sort_order', 'name'], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
