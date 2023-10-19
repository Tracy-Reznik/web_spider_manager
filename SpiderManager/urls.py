"""SpiderManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView

from SpiderManager import views

urlpatterns = [
    path("download_test/<path:filepath>", views.dowmload_test),
    path("delete_test", views.delete_test),
    path("", views.index),
    path('favicon.ico', RedirectView.as_view(url='/static/assets/svg/vue-5532db34.svg')),
    path("update_file_test", views.upd_test),
    path("update_ByetsIO_test", views.upd_ByetsIO_test),
    path("spider_test", views.spider_test)
]
