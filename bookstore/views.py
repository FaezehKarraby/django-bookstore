from django.shortcuts import render

def index(request):
    return render(request,'bookstore/index.html',context={'user':request.user})

def about(request):
    return render(request,'bookstore/about.html')