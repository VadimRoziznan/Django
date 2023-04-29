from django.shortcuts import render


DATA = {
    "omlet": {
        "яйца, шт": 2,
        "молоко, л": 0.1,
        "соль, ч.л.": 0.5,
    },
    "pasta": {
        "макароны, г": 0.3,
        "сыр, г": 0.05,
    },
    "buter": {
        "хлеб, ломтик": 1,
        "колбаса, ломтик": 1,
        "сыр, ломтик": 1,
        "помидор, ломтик": 1,
    },
}


def home_view(request):
    return render(request, "calculator/title.html")


def recipe_view(request):
    try:
        count = int(request.GET.get("servings", 1))
    except:
        count = 1
    name_recipe = request.path.replace("/", "")
    context = {"recipe": DATA.get(name_recipe).copy()}
    for key, item in context["recipe"].items():
        context["recipe"][key] = round(item * count, 2)
    return render(request, "calculator/index.html", context)
