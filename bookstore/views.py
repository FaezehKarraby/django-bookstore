from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def index(request):
    context = {'user': request.user,'genres':models.Book.choice_genre}
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


def about(request):
    return render(request, 'bookstore/about.html')

def genre(request,gn):
    context={'books': None,'genres':models.Book.choice_genre}
    book_list = models.Book.objects.filter(genre=gn)
    if request.GET.get('p'):
        page = request.GET['p']
    else:
        page = 1
    if book_list.exists():
        paginator = Paginator(book_list, 9)
        books = paginator.get_page(page)
        context['books'] = books
    return render(request,'bookstore/gener.html',context=context)

def page_not_found(request, exception):
    return render(request, '404.html')
