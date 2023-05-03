from django.shortcuts import render, redirect
from django.http import HttpResponse
from phones.models import Phone
import re

def index(request):
    return redirect('catalog')


def show_catalog(request):
    phone_objects = Phone.objects.all()
    phones = [
        {
            'name': phone.name, 'price': phone.price, 'image': phone.image,
            'release_date': phone.release_date, 'lte_exists': phone.lte_exists,
            'slug': phone.slug
        } for phone in phone_objects
    ]
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    pattern = r"(/catalog/)|(/)"
    t = request.path
    path1 = re.match(pattern, t)
    print(path1)
    template = 'product.html'
    context = {}
    return render(request, template, context)
