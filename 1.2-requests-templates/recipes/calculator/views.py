from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def home_view(request):
    msg = 'Добро пожаловать.'
    return render(request, 'calculator/title.html')


def omlet_view(request):
    try:
        count = int(request.GET.get("servings", 1))
        print(request)
    except:
        count = 1
    context = {
      'recipe': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
      }
    }
    for key, item in context['recipe'].items():
        context['recipe'][key] = item * count
    return render(request, 'calculator/index.html', context)


def pasta_view(request):
    try:
        count = int(request.GET.get("servings", 1))
    except:
        count = 1
    context = {
      'recipe': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
      }
    }
    for key, item in context['recipe'].items():
        context['recipe'][key] = item * count
    return render(request, 'calculator/index.html', context)


def buter_view(request):
    try:
        count = int(request.GET.get("servings", 1))
    except:
        count = 1
    context = {
      'recipe': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
      }
    }
    for key, item in context['recipe'].items():
        context['recipe'][key] = item * count
    return render(request, 'calculator/index.html', context)


# def buter_view1(request):
#     count = int(request.GEt.get("servings", 1))
#     return HttpResponse(count)


# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
