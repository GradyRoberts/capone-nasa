from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
import requests
import datetime

from .forms import BasicSearchForm, AdvancedSearchForm


def home(request):
    """
    Display current NASA astronomy picture
    of the day from the APOD API. The JSON 
    response is cached to allow quicker 
    load times.
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

    base_form = BasicSearchForm()

    return render(request, 'core/home.html', {
        'base_form': base_form,
        'url': apod_data['url'],
        'title': apod_data['title'],
        'explanation': apod_data['explanation']
    })


def results(request):
    """
    If the request is POST, validate the form data,
    make the API request, extract results,
    and send results to a template to be displayed.
    """
    if request.method == 'GET':
        base_form = BasicSearchForm()
        form = BasicSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            response = requests.get(
                'https://images-api.nasa.gov/search?q=' + query + '&media_type=image')
            response_json = response.json()
            hits = response_json['collection']['metadata']['total_hits']
            items = response_json['collection']['items']
            return render(request, 'core/results.html', {
                'base_form': base_form,
                'hits': hits,
                'items': items
            })
    else:
        return redirect('/')


def advanced_search(request):
    """
    Take in advanced search parameters and make
    API request. Extract results and pass to
    template to render.
    """
    base_form = BasicSearchForm()
    form = AdvancedSearchForm()
    return render(request, 'core/advanced_search.html', {
        'base_form': base_form,
        'form': form
    })


def advanced_results(request):
    """
    If the request is POST, validate the form data,
    make the API request, extract results,
    and send results to a template to be displayed.
    """
    if request.method == 'POST':
        base_form = BasicSearchForm()
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            response = requests.get(
                'https://images-api.nasa.gov/search?q=' + query + '&media_type=image')
            response_json = response.json()
            hits = response_json['collection']['metadata']['total_hits']
            items = response_json['collection']['items']
            return render(request, 'core/results.html', {
                'base_form': base_form,
                'hits': hits,
                'items': items
            })
    else:
        return redirect('/')
