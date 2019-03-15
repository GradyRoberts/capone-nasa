from django.conf import settings
from django.shortcuts import render
import requests

# Create your views here.


def home(request):
    is_cached = ('apod' in request.session)

    if not is_cached:
        response = requests.get(
            'https://api.nasa.gov/planetary/apod?api_key=%s' % settings.NASA_API_KEY)
        request.session['apod'] = response.json()

    apod_data = request.session['apod']

    return render(request, 'core/home.html', {
        'url': apod_data['url'],
        'title': apod_data['title'],
        'explanation': apod_data['explanation'],
        'was_cached': is_cached
    })
