INGREDIENT_TRANSLATION = {
    'яйца': 'eggs', 'яйцо': 'egg',
    'молоко': 'milk', 'мука': 'flour', 'сахар': 'sugar',
    'масло': 'butter', 'сливочное масло': 'butter',
    'помидор': 'tomato', 'помидоры': 'tomatoes',
    'огурец': 'cucumber', 'огурцы': 'cucumbers',
    'сыр': 'cheese', 'творог': 'cottage cheese',
    'курица': 'chicken', 'куриное филе': 'chicken breast',
    'говядина': 'beef', 'свинина': 'pork', 'индейка': 'turkey',
    'ветчина': 'ham', 'колбаса': 'sausage',
    'лосось': 'salmon', 'тунец': 'tuna', 'креветки': 'shrimp',
    'лук': 'onion', 'чеснок': 'garlic',
    'соль': 'salt', 'перец': 'pepper',
    'оливковое масло': 'olive oil', 'подсолнечное масло': 'vegetable oil',
    'сметана': 'sour cream', 'сливки': 'cream', 'йогурт': 'yogurt',
    'свекла': 'beetroot', 'свёкла': 'beetroot',
    'картофель': 'potato', 'картошка': 'potato',
    'морковь': 'carrot', 'капуста': 'cabbage',
    'перец сладкий': 'bell pepper', 'баклажан': 'eggplant',
    'цуккини': 'zucchini', 'грибы': 'mushrooms',
    'рис': 'rice', 'гречка': 'buckwheat', 'овсянка': 'oats',
    'макароны': 'pasta', 'лапша': 'noodles', 'хлеб': 'bread',
    'яблоки': 'apples', 'бананы': 'bananas', 'лимоны': 'lemons',
    'мёд': 'honey', 'мед': 'honey',
    'томатная паста': 'tomato paste', 'майонез': 'mayonnaise',
    'кальмар': 'squid', 'сельдь': 'herring',
    'апельсины': 'oranges', 'клубника': 'strawberries', 'вишня': 'cherries',
    'кокосовое масло': 'coconut oil', 'разрыхлитель': 'baking powder',
    'ваниль': 'vanilla', 'лавровый лист': 'bay leaf',
    'куркума': 'turmeric', 'паприка': 'paprika', 'кориандр': 'coriander',
    'зелень': 'parsley', 'укроп': 'dill', 'петрушка': 'parsley',
    'фундук': 'hazelnuts', 'изюм': 'raisins', 'курага': 'dried apricots',
    'миндаль': 'almonds', 'грецкие орехи': 'walnuts',
    'фасоль': 'beans', 'горох': 'peas', 'чечевица': 'lentils',
}


def translate_ingredients(ingredient_list):
    translated = []
    for ing in ingredient_list:
        key = ing.strip().lower()
        eng = INGREDIENT_TRANSLATION.get(key)
        translated.append(eng if eng else ing)
    return translated
