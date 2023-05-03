from django.shortcuts import render, redirect
from phones.models import Phone

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
    template = 'product.html'
    context = {}
    return render(request, template, context)
