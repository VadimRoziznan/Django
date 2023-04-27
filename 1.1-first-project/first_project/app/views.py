import os
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, reverse



def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_date = datetime.today().strftime("%d.%m.%Y")
    current_time = datetime.today().strftime("%H:%M:%S")
    msg = f'Текущее время: {current_time} Текущая дата: {current_date}'
    return HttpResponse(msg)


def workdir_view(request):
    dir_path = ' '.join(os.listdir())
    return HttpResponse(dir_path)
