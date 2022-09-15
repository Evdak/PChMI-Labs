from django.contrib import admin
from django.urls import path
from pywebio.platform.django import webio_view
from .main import main

webio_view_func = webio_view(main)

urlpatterns = [
    path('', webio_view_func),
]
