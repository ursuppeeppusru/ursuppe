# ps_list/views.py
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.db.models import Q
from itertools import chain

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission


def trim_whitespaces(list):
    # trim whitespaces in newline
    result = []
    for i in list:
        result.append(i.lstrip(' '))

    return result

def strip_start_end(list):
    # strip start and end spaces
    result = []
    for i in list:
        result.append(i.strip())

    return result

def unique(list):
    # remove duplicates from list
    result = []
    for i in list:
        if i not in result:
            result.append(i)

    return result

def today():
    today = timezone.now().date()
    return today

# Index
def compile_list(list_type):
    if list_type is 'photographer':
        submissions = (ExhibitionSubmission.objects.filter(published=True).values(list_type))
        combined = list(submissions)
    else:
        submissions = (ExhibitionSubmission.objects.filter(published=True).values(list_type))
        events = (CalendarSubmission.objects.filter(published=True).values(list_type))
        combined = list(chain(submissions, events))

    result = []
    # loop through, split by comma and join into one list
    for i in combined:
        if ',' in i[list_type]:
            i_split_by_comma = i[list_type].split(',')
            result.extend(i_split_by_comma)
        else:
            result.append(i[list_type])

    result = trim_whitespaces(result)
    result = unique(result)
    # sort alphabetically
    result = sorted(result,key=str.lower)

    return result

# Current and upcoming
def compile_list_current(list_type):
    # submissions = (ExhibitionSubmission.objects.filter(published=True).values(list_type))
    events = (CalendarSubmission.objects.filter(published=True).filter(Q(exhibition_end__gte=today()) | Q(opening=today())).values(list_type))
    combined = list(events)

    result = []
    # loop through, split by comma and join into one list
    for i in combined:
        if ',' in i[list_type]:
            i_split_by_comma = i[list_type].split(',')
            result.extend(i_split_by_comma)
        else:
            result.append(i[list_type])

    result = trim_whitespaces(result)
    result = strip_start_end(result)
    result = unique(result)
    # sort alphabetically
    result = sorted(result,key=str.lower)

    return result


# Index
@cache_page(60 * 60)
def list_artists(request):
    return render(request, 'list_artists.html', {'list': compile_list('artists')})

@cache_page(60 * 60)
def list_curators(request):
    return render(request, 'list_curators.html', {'list': compile_list('curators')})

@cache_page(60 * 60)
def list_photographers(request):
    return render(request, 'list_photographers.html', {'list': compile_list('photographer')})

@cache_page(60 * 60)
def list_locations(request):
    return render(request, 'list_locations.html', {'list': compile_list('location')})

@cache_page(60 * 60)
# Current and upcoming
def list_current_artists(request):
    return render(request, 'list_artists.html', {'list': compile_list_current('artists')})

@cache_page(60 * 60)
def list_current_curators(request):
    return render(request, 'list_curators.html', {'list': compile_list_current('curators')})

@cache_page(60 * 60)
def list_current_locations(request):
    return render(request, 'list_locations.html', {'list': compile_list_current('location')})
