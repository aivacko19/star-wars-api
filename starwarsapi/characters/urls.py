from django.contrib import admin
from django.urls import include, path

from characters import views

urlpatterns = [
    path('collections/', views.index, name="index"),
]