"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name="main"

urlpatterns = [
    path('', views.index, name="index"),
	path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('register/', views.register, name="register"),
	path('<a_slug>/upload_photo/', views.upload_photo, name="upload_photo"),
    path('add_new/', views.add_new, name="add_new"),
    path('delete_obj/<int:pk>/<int:c_album>/<int:level>/', views.delete_obj, name="delete_obj"),
	path('<single_slug>', views.single_slug, name="single_slug"),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)