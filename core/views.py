from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
import requests
import datetime
import urllib.parse

from .forms import BasicSearchForm, AdvancedSearchForm


def home(request):
    form = BasicSearchForm()
    return render(request, 'core/home.html', {
        'form': form
    })


def apod(request):
    """
    Display current NASA astronomy picture
    of the day from the APOD API.
    """
    response = requests.get(
        'https://api.nasa.gov/planetary/apod?api_key=%s' % settings.NASA_API_KEY).json()

    apod_data = response

    return render(request, 'core/apod.html', {
        'url': apod_data['url'],
        'title': apod_data['title'],
        'explanation': apod_data['explanation'],
        'media_type': apod_data['media_type']
    })


def results(request):
    """
    Validate the form data,
    make the API request, extract results,
    and send results to a template to be displayed.
    Results are paginated with 100 items per page.
    100 is chosen because it matches how the NASA
    results are paginated, making queries easier.
    """
    form = BasicSearchForm(request.GET)
    if form.is_valid():
        page = request.GET.get('results_page', '1')
        query = 'q=' + \
            form.cleaned_data.get('q') + \
            '&media_type=image' + '&page=' + page

        response = requests.get(
            'https://images-api.nasa.gov/search?' + query).json()

        hits = response['collection']['metadata']['total_hits']
        item_list = response['collection']['items']

        num_pages = hits // 100
        remainder = hits % 100

        page = int(page)
        lower = ((page-1)*100+1) if page > 1 else 1
        upper = (page*100) if page > 1 else 100
        upper = upper if upper <= hits else hits

        search_again_form = BasicSearchForm()
        return render(request, 'core/results.html', {
            'query': query,
            'hits': hits,
            'items': item_list,
            'form': search_again_form,
            'page': page,
            'num_pages': num_pages,
            'next_page': page+1,
            'prev_page': page-1,
            'lower': lower,
            'upper': upper
        })


def advanced_search(request):
    """
    Take in advanced search parameters and
    send to advanced_results view for
    display.
    """
    form = AdvancedSearchForm()
    return render(request, 'core/advanced_search.html', {
        'form': form
    })


def advanced_results(request):
    """
    Validate the form data,
    make the API request, extract results,
    and send results to a template to be displayed.
    Results are paginated with 25 items per page.
    """
    form = AdvancedSearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        keywords = form.cleaned_data.get('keywords')
        location = form.cleaned_data.get('location')
        photographer = form.cleaned_data.get('photographer')
        year_start = form.cleaned_data.get('year_start')
        year_end = form.cleaned_data.get('year_end')
        nasa_id = form.cleaned_data.get('nasa_id')

        page = request.GET.get('results_page', '1')
        params = {
            'media_type': 'image',
            'page': page
        }
        if title != None:
            params['title'] = title
        if keywords != None:
            params['keywords'] = keywords
        if location != None:
            params['location'] = location
        if photographer != None:
            params['photographer'] = photographer
        if year_start != None:
            params['year_start'] = year_start
        if year_end != None:
            params['year_end'] = year_end
        if nasa_id != None:
            params['nasa_id'] = nasa_id

        query = urllib.parse.urlencode(params)
        response = requests.get(
            'https://images-api.nasa.gov/search?' + query).json()

        hits = response['collection']['metadata']['total_hits']
        item_list = response['collection']['items']

        num_pages = hits // 100
        remainder = hits % 100

        page = int(page)
        lower = ((page-1)*100+1) if page > 1 else 1
        upper = (page*100) if page > 1 else 100
        upper = upper if upper <= hits else hits

        search_again_form = BasicSearchForm()
        return render(request, 'core/results.html', {
            'query': query,
            'hits': hits,
            'items': item_list,
            'form': search_again_form,
            'page': page,
            'num_pages': num_pages,
            'next_page': page+1,
            'prev_page': page-1,
            'lower': lower,
            'upper': upper
        })


def detail(request):
    """
    Show the image in full size along with its
    metadata.
    """
    if request.method == 'GET':
        pass
