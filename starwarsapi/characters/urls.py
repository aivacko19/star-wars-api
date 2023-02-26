from django.contrib import admin
from django.urls import include, path

from characters import views

urlpatterns = [
    path('', views.index, name="index"),
    path('collections/', views.index, name="index"),
    path('collections/fetch/', views.fetch, name="fetch"),
    path('collections/<filename>/', views.detail, name="detail"),
    path('collections/<filename>/value-count/', views.value_count, name="value-count"),
]