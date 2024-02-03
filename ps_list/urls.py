# ps_list/urls.py
from django.urls import path
from .views import list_artists, list_curators, list_locations

urlpatterns = [
    path('artists/', list_artists, name='list_artists'),
    path('curators/', list_curators, name='list_curators'),
    path('locations/', list_locations, name='list_locations'),
    # Add more patterns as needed
]