from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms, models


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.SignUP(request.POST)
            if form.is_valid():
                user = User.objects.create_user(form.cleaned_data['email'], password=form.cleaned_data['password'],
                                                first_name=form.cleaned_data['first_name'])
                models.Profile.objects.create(user=user)
                return render(request, 'accounts/user.html')
        else:
            form = forms.SignUP()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context=context)
    else:
        return HttpResponseRedirect(reverse('bookstore:index'))


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('accounts:login'))
    return HttpResponseRedirect(reverse('bookstore:index'))


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.Login(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
                if user:
                    context = {'form': form, 'user': user}
                    login(request, user=user)
                    if request.GET.get('next'):
                        return HttpResponseRedirect(request.GET['next'])
                    return render(request, 'accounts/succeed_login.html', context=context)
                else:
                    context = {'form': form, 'error': 'email or password is wrong'}
            else:
                context = {'form': form}
        else:
            form = forms.Login()
            context = {'form': form}
        return render(request, 'accounts/login.html', context=context)
    else:
        return HttpResponseRedirect(reverse('bookstore:index'))


@login_required
def profile(request):
    context = {'user': request.user}
    if request.method == 'POST':
        form = forms.Profile(request.POST, request.FILES)
        if form.is_valid():
            if request.user.first_name != form.cleaned_data['first_name']:
                context['update'] = True
                request.user.first_name = form.cleaned_data['first_name']
                request.user.save()
            if form.cleaned_data.get('image'):
                context['update'] = True
                request.user.profile.image = form.cleaned_data['image']
                request.user.profile.save()
    else:
        form = forms.Profile()
    context['form'] = form
    return render(request, 'accounts/profile.html', context=context)


@login_required()
def change_password(request):
    context = {'update': False}
    if request.method == 'POST':
        form = forms.Change_password(request.POST, user=request.user)
        if form.is_valid():
            context['update'] = True
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            return render(request,'accounts/succeed_change_password.html')
    else:
        form = forms.Change_password(user=request.user)
    context['form'] = form
    return render(request, 'accounts/change_password.html',context=context)
