# ps_list/views.py
from django.shortcuts import render

from itertools import chain
from django.utils import timezone

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission


def trim_whitespaces(list):
    # trim whitespaces in newline
    result = []
    for i in list:
        result.append(i.lstrip(' '))

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
    events = (CalendarSubmission.objects.filter(published=True).filter(exhibition_end__gte=today()).values(list_type))
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
    result = unique(result)
    # sort alphabetically
    result = sorted(result,key=str.lower)

    return result


# Index
def list_artists(request):
    return render(request, 'list_artists.html', {'list': compile_list('artists')})


def list_curators(request):
    return render(request, 'list_curators.html', {'list': compile_list('curators')})


def list_locations(request):
    return render(request, 'list_locations.html', {'list': compile_list('location')})

# Current and upcoming
def list_current_artists(request):
    return render(request, 'list_artists.html', {'list': compile_list_current('artists')})


def list_current_curators(request):
    return render(request, 'list_curators.html', {'list': compile_list_current('curators')})


def list_current_locations(request):
    return render(request, 'list_locations.html', {'list': compile_list_current('location')})
