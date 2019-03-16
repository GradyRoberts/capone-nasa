from django.conf import settings
from django.shortcuts import render
import requests
import datetime

# Create your views here.


def home(request):
    """
    Home page view displays current NASA astronomy picture
    of the day from the APOD API. The JSON response is cached
    to allow quicker load times.
    """
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")

    is_cached = ('apod' in request.session)
    is_cached_and_current = False
    if is_cached:
        is_cached_and_current = (request.session['apod']['date'] == today)

    if not is_cached_and_current:
        response = requests.get(
            'https://api.nasa.gov/planetary/apod?api_key=%s' % settings.NASA_API_KEY)
        request.session['apod'] = {
            'data': response.json(),
            'date': today
        }

    apod_data = request.session['apod']['data']

    return render(request, 'core/home.html', {
        'url': apod_data['url'],
        'title': apod_data['title'],
        'explanation': apod_data['explanation']
    })
