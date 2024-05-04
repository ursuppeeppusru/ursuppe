# ps_calendar/urls.py
from django.urls import path

from .views import EventFeed, feed_information

urlpatterns = [
    path('', feed_information, name='feed_information'),
    path('current-and-upcoming/ical', EventFeed()),
    # Add more patterns as needed
]
