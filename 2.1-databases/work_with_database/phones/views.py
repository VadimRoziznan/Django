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
    options_name = request.GET.get('sort')
    if options_name:
        phones = options(options_name, phones)
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_objects = Phone.objects.filter(slug=slug)
    phone = [
        {
            'name': phone.name, 'price': phone.price, 'image': phone.image,
            'release_date': phone.release_date, 'lte_exists': phone.lte_exists,
            'slug': phone.slug
        } for phone in phone_objects
    ][0]
    context = {'phone': phone}
    return render(request, template, context)


def options(parameter, data):
    if parameter == 'name':
        data.sort(key=lambda key: key['name'])
    elif parameter == 'max_price':
        data.sort(key=lambda key: key['price'], reverse=True)
    elif parameter == 'min_price':
        data.sort(key=lambda key: key['price'])
    return data
