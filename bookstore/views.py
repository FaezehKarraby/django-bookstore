from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def index(request):
    context = {'genres': models.Book.choice_genre}
    if request.GET.get('p'):
        page = request.GET['p']
    else:
        page = 1
    context['query'] = request.GET.get('q')
    if context['query']:
        book_list = models.Book.objects.filter(book__contains=request.GET['q'])
        if book_list.exists():
            paginator = Paginator(book_list, 9)
            books = paginator.get_page(page)
            context['books'] = books
            context['query'] = request.GET['q']
    return render(request, 'bookstore/index.html', context=context)


def index_api(request):
    if request.GET.get('p'):
        page = request.GET['p']
    else:
        page = 1
    if request.GET.get('q'):
        book_list = models.Book.objects.filter(book__contains=request.GET['q'])
        if book_list.exists():
            paginator = Paginator(book_list, 9)
            books = paginator.get_page(page)
            data = {
                'ok': True,
                'page': page,
                'total_pages': books.paginator.num_pages,
                'results': [{'name': book.book,
                             'genre': book.get_genre_display(),
                             'description': book.description,
                             'price': book.price,
                             'image': settings.MEDIA_URL+book.image.name
                             } for book in books]
            }
            return JsonResponse(data)
    return JsonResponse({'ok': False, 'result': 'no parameter'})


def about(request):
    return render(request, 'bookstore/about.html',context={'genres': models.Book.choice_genre})


def genre(request, gn):
    context = {'books': None, 'genres': models.Book.choice_genre}
    book_list = models.Book.objects.filter(genre=gn)
    if request.GET.get('p'):
        page = request.GET['p']
    else:
        page = 1
    if book_list.exists():
        paginator = Paginator(book_list, 9)
        books = paginator.get_page(page)
        context['books'] = books
    return render(request, 'bookstore/gener.html', context=context)

def genre_api(request, gn):
    book_list = models.Book.objects.filter(genre=gn)
    if request.GET.get('p'):
        page = request.GET['p']
    else:
        page = 1
    if book_list.exists():
        paginator = Paginator(book_list, 9)
        books = paginator.get_page(page)
        data = {
            'ok': True,
            'page': page,
            'total_pages': books.paginator.num_pages,
            'results': [{'name': book.book,
                         'genre': book.get_genre_display(),
                         'description': book.description,
                         'price': book.price,
                         'image': settings.MEDIA_URL + book.image.name
                         } for book in books]
        }
        return JsonResponse(data)

def page_not_found(request, exception):
    return render(request, '404.html')
