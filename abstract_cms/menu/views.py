from django.shortcuts import render
from django.urls import resolve


def menu_view(request):
    return render(request, 'base.html', {'current_url': [request.path, resolve(request.path).url_name]})
