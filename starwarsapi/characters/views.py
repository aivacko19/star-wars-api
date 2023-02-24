from django.shortcuts import render

from characters.models import Collection

def index(request, **kwargs):
    collections = Collection.objects.all()
    return render(request, "index.html", {"title": "Collections", "collections": collections})
