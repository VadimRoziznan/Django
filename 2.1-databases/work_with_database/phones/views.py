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
    phone_name = request.path.split('/')[-2]
    template = 'product.html'
    phone_objects = Phone.objects.filter(slug=phone_name)
    phone = [
        {
            'name': phone.name, 'price': phone.price, 'image': phone.image,
            'release_date': phone.release_date, 'lte_exists': phone.lte_exists,
            'slug': phone.slug
        } for phone in phone_objects
    ][0]
    print('phone', phone)
    context = {'phone': phone}
    return render(request, template, context)
