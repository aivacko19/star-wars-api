from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings

import requests
from datetime import datetime
import csv

from characters.models import Collection


SWAPI_PEOPLE_URL = "https://swapi.dev/api/people"


@require_http_methods(['GET'])
def index(request, **kwargs):
    collections = Collection.objects.all()
    return render(request, "index.html", {"title": "Collections", "collections": collections})


@require_http_methods(['POST'])
def fetch(request, **kwargs):

    r = requests.get(SWAPI_PEOPLE_URL).json()
    
    # Ignore fetch and return if result is empty
    if not r['results']:
        return redirect('index')

    dt = datetime.now()
    filename = dt.strftime("%Y%m%d%H%M%S.csv")

    # Add verbose name field to collection
    # name = dt.strftime("%b. %d, %Y, %I:%M %p")

    with open(settings.SWAPI_CSV_DIR / filename, 'w') as csvfile:

        total_count = r['count']
        counter = 0

        field_names = list(r['results'][0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(r['results'])
        counter += len(r['results'])
        
        while counter < total_count:
            r = requests.get(r['next']).json()
            writer.writerows(r['results'])
            counter += len(r['results'])

    Collection.objects.create(filename=filename)
    
    return redirect('index')
