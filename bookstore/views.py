from django.shortcuts import render
from . import models


def index(request):
    context = {'user': request.user}
    if request.GET.get('p'):
        page = int(request.GET['p'])
        if page == 0:
            page = 1
        else:
            page = abs(page)
    else:
        page = 1
    if request.GET.get('q'):
        page -= 1
        books = models.Book.objects.filter(book__contains=request.GET['q'])
        context['cn'] = len(books)
        cn_res = page * 9
        if context['cn'] >= cn_res:
            books = books[cn_res:cn_res + 9]
            context['books'] = books
        else:
            return render(request,'404.html')
    return render(request, 'bookstore/index.html', context=context)


def about(request):
    return render(request, 'bookstore/about.html')

def page_not_found(request,exception):
    return render(request, '404.html')