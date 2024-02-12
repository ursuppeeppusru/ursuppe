# ps_list/views.py
from django.shortcuts import render

from itertools import chain

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


def first_letter(self):
        return self.name and self.name[0] or ''


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


def list_artists(request):
    return render(request, 'list_artists.html', {'list': compile_list('artists')})


def list_curators(request):
    return render(request, 'list_curators.html', {'list': compile_list('curators')})


def list_locations(request):
    return render(request, 'list_locations.html', {'list': compile_list('location')})
