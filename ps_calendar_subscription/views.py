from django.shortcuts import render
from django_ical.views import ICalFeed
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.db.models import Q

from ps_calendar.models import CalendarSubmission

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def today():
    today = timezone.now().date()
    return today


class EventFeed(ICalFeed):
    """
    Events feed for current and upcoming
    """

    title = env('SITE_NAME')
    description = 'Current and upcoming events'
    product_id = '-//current-and-upcoming//EN'
    timezone = 'GMT+1'
    file_name = "ursuppe_current-and-upcoming.ics"

    def items(self):
        return CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_end__gte=today()) | Q(opening__gte=today()))

    def item_title(self, item):
        title = item.event_type + ': ' + item.project_title
        return title

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        if item.one_day_event == True:
            return item.opening
        else:
            return item.exhibition_opening

    def item_end_datetime(self, item):
        if item.one_day_event == True:
            return item.opening
        else:
            return item.exhibition_end

    def item_location(self, item):
    	location = item.location + ' (' + item.location_address + ')'
    	return location

# Past events
@cache_page(60 * 60)
def feed_information(request):
    return render(request, 'feed_information.html')