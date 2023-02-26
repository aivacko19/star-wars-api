from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings

import requests
from datetime import datetime
import petl

from characters.models import Collection


@require_http_methods(['GET'])
def index(request, *args, **kwargs):
    collections = Collection.objects.order_by('-created_at')
    data = {
        'title': "Collections",
        'collections': collections,
    }
    return render(request, "index.html", data)


@require_http_methods(['POST'])
def fetch(request, *args, **kwargs):

    url = "https://swapi.dev/api/people"
    r = requests.get(url).json()
    
    # Ignore fetch and return if result is empty
    if not r['results']:
        return redirect('index')

    # Prepare collection entry fields
    dt = datetime.now()
    filename = dt.strftime("%Y%m%d%H%M%S")
    name = dt.strftime("%b. %d, %Y, %I:%M %p")

    csvfile = settings.SWAPI_CSV_DIR / f'{filename}.csv'
    homeworld_map = {}
    
    while True:
        table = petl.fromdicts(r['results'])

        # Add date column
        table = petl.addfield(table, 'date', lambda row: row.edited[:10])

        # Iterate distinct homeworld values and fetch them
        homeworld_urls = set(petl.values(table, 'homeworld'))
        for homeworld_url in homeworld_urls:
            if homeworld_url not in homeworld_map:
                homeworld_map[homeworld_url] = requests.get(homeworld_url).json()['name']

        # Resolve homeworld column
        table = petl.convert(table, 'homeworld', homeworld_map)

        # Drop unused fields
        unused_fields = [
            'films',
            'species',
            'vehicles',
            'starships',
            'created',
            'edited',
            'url',
        ]
        table = petl.cutout(table, *unused_fields)

        if not csvfile.exists():
            petl.tocsv(table, csvfile)
        else:
            petl.appendcsv(table, csvfile)
        
        if not r['next']:
            break
        r = requests.get(r['next']).json()

    # Save collection entry
    Collection.objects.create(filename=filename, name=name)
    
    return redirect('index')


@require_http_methods(['GET'])
def detail(request, filename, *args, **kwargs):

    csvfile = settings.SWAPI_CSV_DIR / f'{filename}.csv'
    table = petl.fromcsv(csvfile)

    num = int(request.GET.get('num', 10))
    table = petl.head(table, n=num)
    
    data = {
        'title': csvfile.name,
        'filename': csvfile.name,
        'header': petl.header(table),
        'data': petl.data(table),
        'num': num + 10, 
    }
    return render(request, "detail.html", data)

