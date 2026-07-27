"""Фото продуктов: Spoonacular CDN + Wikimedia Commons (резерв)."""

from pathlib import Path
from urllib.parse import quote

SPOONACULAR_CDN = 'https://img.spoonacular.com/ingredients_250x250'
PHOTOS_STATIC_DIR = 'img/products-photos'
WIKIMEDIA_UA = 'FridgeRecipesPortfolio/1.0 (portfolio demo; github.com/Alexandr-mailru)'

# Проверено по CDN Spoonacular (ingredients_250x250)
PRODUCT_PHOTOS = {
    'kuritsa': 'chicken-breasts.jpg',
    'govyadina': 'beef-cubes-raw.png',
    'svinina': 'pork-tenderloin-raw.png',
    'indeyka': 'turkey-drumstick.jpg',
    'vetchina': 'ham.jpg',
    'kolbasa': 'raw-pork-sausage.png',
    'losos': 'salmon.jpg',
    'tunets': 'canned-tuna.png',
    'krevetki': 'shrimp.jpg',
    'pomidory': 'tomato.png',
    'ogurtsy': 'cucumber.jpg',
    'luk': 'brown-onion.png',
    'chesnok': 'garlic.jpg',
    'morkov': 'sliced-carrot.png',
    'kartofel': 'potatoes-yukon-gold.png',
    'kapusta': 'cabbage.jpg',
    'perets-sladkiy': 'bell-pepper-orange.png',
    'baklazhan': 'eggplant.jpg',
    'tsukkini': 'zucchini.jpg',
    'svyokla': 'beets.jpg',
    'griby': 'mushrooms.jpg',
    'yabloki': 'apple.jpg',
    'banany': 'bananas.jpg',
    'apelsiny': 'orange.jpg',
    'klubnika': 'strawberries.jpg',
    'limony': 'lemon.jpg',
    'vishnya': 'cherries.jpg',
    'moloko': 'milk.jpg',
    'syr': 'cheddar-cheese.jpg',
    'slivochnoe-maslo': 'butter.jpg',
    'smetana': 'sour-cream.jpg',
    'yogurt': 'plain-yogurt.jpg',
    'tvorog': 'cottage-cheese.jpg',
    'yaytsa': 'egg.jpg',
    'muka': 'flour.jpg',
    'sahar': 'white-sugar.jpg',
    'med': 'honey.jpg',
    'vanil': 'vanilla.jpg',
    'makarony': 'spaghetti.jpg',
    'lapsha': 'egg-noodles.jpg',
    'hleb': 'white-bread.jpg',
    'olivkovoe-maslo': 'olive-oil.jpg',
    'podsolnechnoe-maslo': 'vegetable-oil.jpg',
    'kokosovoe-maslo': 'coconut-oil.jpg',
    'sol': 'salt.jpg',
    'perec': 'black-pepper.jpg',
    'kurkuma': 'turmeric.jpg',
    'paprika': 'paprika.jpg',
    'koriandr': 'coriander-seeds.jpg',
    'lavrovyy-list': 'bay-leaves.jpg',
    'zelen': 'parsley.jpg',
    'ukrop': 'dill.jpg',
    'ris': 'uncooked-white-rice.png',
    'ovsyanka': 'rolled-oats.jpg',
    'chechevitsa': 'lentils-brown.jpg',
    'fasol': 'kidney-beans.jpg',
    'goroh': 'peas.jpg',
    'mindal': 'almonds.jpg',
    'gretskie-orehi': 'walnuts.jpg',
    'funduk': 'hazelnuts.jpg',
    'izyum': 'raisins.jpg',
    'kuraga': 'dried-apricots.jpg',
    'tomatnaya-pasta': 'tomato-paste.jpg',
    'mayonez': 'mayonnaise.jpg',
}

# Wikimedia Commons — только если нет на CDN Spoonacular
WIKIMEDIA_PHOTOS = {
    'kalmary': 'Squid.jpg',
    'seld': 'Herring.jpg',
    'slivki': 'Cream.jpg',
    'razryhlitel': 'Baking_soda.jpg',
    'grechka': 'Grechka.jpg',
}

PHOTO_FALLBACKS = {
    'kuritsa': ['chicken-breasts.png'],
    'tvorog': ['ricotta.png', 'cottage-cheese.png'],
    'vanil': ['vanilla-extract.jpg'],
    'syr': ['cheddar-cheese.png'],
    'losos': ['salmon.png'],
    'vetchina': ['ham.png'],
}


def cdn_url(photo_name):
    if not photo_name:
        return ''
    return f'{SPOONACULAR_CDN}/{photo_name}'


def wikimedia_url(filename):
    return f'https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width=250'


def photo_name_for_slug(slug):
    return PRODUCT_PHOTOS.get(slug, '')


def photo_names_to_try(slug):
    names = []
    primary = PRODUCT_PHOTOS.get(slug)
    if primary:
        names.append(primary)
    names.extend(PHOTO_FALLBACKS.get(slug, []))
    return names


def local_photo_path(slug):
    from django.conf import settings

    photos_dir = Path(settings.BASE_DIR) / 'static' / PHOTOS_STATIC_DIR
    for ext in ('.png', '.jpg', '.jpeg', '.webp'):
        path = photos_dir / f'{slug}{ext}'
        if path.exists():
            return f'/static/{PHOTOS_STATIC_DIR}/{slug}{ext}'
    return ''


def photo_url_for_slug(slug):
    cached = local_photo_path(slug)
    if cached:
        return cached
    name = photo_name_for_slug(slug)
    if name:
        return cdn_url(name)
    if slug in WIKIMEDIA_PHOTOS:
        return wikimedia_url(WIKIMEDIA_PHOTOS[slug])
    return f'/static/img/products/{slug}.svg'


def is_valid_image_response(response):
    content_type = response.headers.get('content-type', '')
    return (
        response.status_code == 200
        and content_type.startswith('image/')
        and len(response.content) > 500
    )
