# ps_list/urls.py
from django.urls import path
from .views import list_artists, list_curators, list_photographers, list_locations, list_current_artists, list_current_curators, list_current_locations

urlpatterns = [
    path('artists/', list_artists, name='list_artists'),
    path('curators/', list_curators, name='list_curators'),
    path('photographers/', list_photographers, name='list_photographers'),
    path('locations/', list_locations, name='list_locations'),
    path('artists/current', list_current_artists, name='list_current_artists'),
    path('curators/current', list_current_curators, name='list_current_curators'),
    path('locations/current', list_current_locations, name='list_current_locations'),
    # Add more patterns as needed
]