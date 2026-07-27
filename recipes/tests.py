from django.core.management import call_command
from django.test import Client, TestCase

from recipes.models import LocalRecipe
from recipes.views import find_local_recipes, get_product_categories


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', verbosity=0)

    def test_product_categories_not_empty(self):
        self.assertGreater(len(get_product_categories()), 0)

    def test_find_local_recipes(self):
        results = find_local_recipes(['яйца', 'картофель', 'лук'])
        self.assertGreater(len(results), 0)
        self.assertTrue(all(r['is_local'] for r in results))


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_catalog', verbosity=0)

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_legal_pages(self):
        for url in ('/about/', '/privacy/', '/copyright/', '/favorites/'):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_local_recipe_detail_and_pdf(self):
        recipe = LocalRecipe.objects.first()
        if not recipe:
            self.skipTest('No recipes in database — run seed_catalog')
        detail = self.client.get(f'/recipe/local_{recipe.id}/')
        self.assertEqual(detail.status_code, 200)
        pdf = self.client.get(f'/recipe/local_{recipe.id}/pdf/')
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf['Content-Type'], 'application/pdf')

    def test_toggle_favorite(self):
        recipe = LocalRecipe.objects.first()
        if not recipe:
            self.skipTest('No recipes in database — run seed_catalog')
        response = self.client.post(f'/favorite/local_{recipe.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_favorite'])

    def test_search_post(self):
        response = self.client.post('/', {'ingredients': 'яйца, картофель', 'max_time': ''})
        self.assertEqual(response.status_code, 200)
