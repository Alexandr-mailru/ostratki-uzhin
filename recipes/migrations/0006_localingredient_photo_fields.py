from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_localrecipe_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='localingredient',
            name='photo_file',
            field=models.CharField(blank=True, help_text='Локальный кэш фото', max_length=120),
        ),
        migrations.AddField(
            model_name='localingredient',
            name='photo_name',
            field=models.CharField(blank=True, help_text='Имя файла на CDN Spoonacular', max_length=120),
        ),
    ]
