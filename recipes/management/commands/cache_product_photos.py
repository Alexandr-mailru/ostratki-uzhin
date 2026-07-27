from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import LocalIngredient
from recipes.product_photos import (
    PHOTOS_STATIC_DIR,
    WIKIMEDIA_PHOTOS,
    WIKIMEDIA_UA,
    cdn_url,
    is_valid_image_response,
    photo_names_to_try,
    wikimedia_url,
)
from recipes.translations import translate_ingredients


class Command(BaseCommand):
    help = 'Скачивает фото продуктов в static/img/products-photos/'

    def handle(self, *args, **options):
        photos_dir = Path(settings.BASE_DIR) / 'static' / PHOTOS_STATIC_DIR
        photos_dir.mkdir(parents=True, exist_ok=True)
        api_key = settings.SPOONACULAR_API_KEY

        ok = 0
        failed = []

        for product in LocalIngredient.objects.exclude(slug=''):
            if self._try_spoonacular(product, photos_dir):
                ok += 1
                self.stdout.write(f'  OK {product.name}')
                continue

            if product.slug in WIKIMEDIA_PHOTOS and self._try_wikimedia(product, photos_dir):
                ok += 1
                self.stdout.write(f'  OK {product.name} (Wikimedia)')
                continue

            if api_key:
                photo_name = self._resolve_via_api(api_key, product.name)
                if photo_name and self._save_image(product, photos_dir, cdn_url(photo_name), photo_name):
                    ok += 1
                    self.stdout.write(f'  OK {product.name} (API)')
                    continue

            failed.append(product.name)

        self.stdout.write(self.style.SUCCESS(f'Скачано: {ok} из {LocalIngredient.objects.count()}'))
        if failed:
            self.stdout.write(self.style.WARNING(f'Не найдено: {", ".join(failed)}'))

    def _try_spoonacular(self, product, photos_dir):
        for photo_name in photo_names_to_try(product.slug):
            if self._save_image(product, photos_dir, cdn_url(photo_name), photo_name):
                return True
        return False

    def _try_wikimedia(self, product, photos_dir):
        filename = WIKIMEDIA_PHOTOS[product.slug]
        return self._save_image(
            product,
            photos_dir,
            wikimedia_url(filename),
            filename,
            headers={'User-Agent': WIKIMEDIA_UA},
        )

    def _save_image(self, product, photos_dir, url, source_name, headers=None):
        ext = Path(source_name).suffix or '.jpg'
        filename = f'{product.slug}{ext}'
        dest = photos_dir / filename

        try:
            response = requests.get(url, timeout=20, headers=headers or {})
            if not is_valid_image_response(response):
                return False
            dest.write_bytes(response.content)
            product.photo_file = filename
            product.photo_name = source_name
            product.save(update_fields=['photo_file', 'photo_name'])
            return True
        except requests.RequestException:
            return False

    def _resolve_via_api(self, api_key, product_name):
        query = translate_ingredients([product_name])[0]
        try:
            response = requests.get(
                'https://api.spoonacular.com/food/ingredients/search',
                params={'query': query, 'number': 1, 'apiKey': api_key},
                timeout=12,
            )
            if response.status_code != 200:
                return ''
            results = response.json().get('results', [])
            if results:
                return results[0].get('image', '')
        except requests.RequestException:
            return ''
        return ''
