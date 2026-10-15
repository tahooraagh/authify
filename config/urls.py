from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import set_language
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
]
