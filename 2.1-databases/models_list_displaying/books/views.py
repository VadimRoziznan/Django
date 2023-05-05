from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import Book
from slugify import slugify


def content():
    books_objects = Book.objects.all()
    CONTENT = [
        {
            'name': book.name, 'author': book.author, 'pub_date': book.pub_date, 'slug': slugify(book.name),
            'page_number': num
        } for num, book in enumerate(books_objects, start=1)
    ]
    return CONTENT


def books_view(request):
    template = 'books/books_list.html'
    CONTENT = content()
    context = {'books': CONTENT}
    return render(request, template, context)


def book_view(request):
    template = 'book.html'
    books_objects = Book.objects.all()
    CONTENT = content()
    dates = [
        {
            'pub_date': book.pub_date
        } for book in books_objects
    ]
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(CONTENT, 1)
    page = paginator.get_page(page_number)
    try:
        next_page = dates[page_number]
    except:
        next_page = dates[page_number - 1]
    try:
        previous_page = dates[page_number - 2]
    except:
        previous_page = dates[page_number + 1]
    context = {
        'book': page,
        'page': page,
        'next_page': next_page,
        'previous_page': previous_page
    }
    return render(request, template, context)
