from django.contrib import admin
from django.urls import path, include

handler404='bookstore.views.page_not_found'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('',include('bookstore.urls')),
]
