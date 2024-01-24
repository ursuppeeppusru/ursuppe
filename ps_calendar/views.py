# ps_calendar/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .forms import CalendarSubmissionForm, CalendarImagesForm
from .models import CalendarImages
from django.contrib import messages

from .models import CalendarSubmission

def calendar_submission_create(request):
    ImageFormSet = modelformset_factory(CalendarImages, form=CalendarImagesForm, extra=1)

    if request.method == 'POST':
        submission_form = CalendarSubmissionForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=CalendarImages.objects.none())

        if submission_form.is_valid() and formset.is_valid():
            submission = submission_form.save()
            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.calendar = submission
                    image.save()

            # Add more logic here if needed, such as redirecting to a success page.
            messages.success(request, "Thank you for submitting your exhibition!" )
            return redirect('/')
        else:
            messages.error(request, "Some error occurred while submitting. Please re-check your form.")
    else:
        submission_form = CalendarSubmissionForm()
        formset = ImageFormSet(queryset=CalendarImages.objects.none())

    return render(request, 'calendar_submission_form.html', {
        'submission_form': submission_form,
        'formset': formset,
    })

def event_list(request):
    # Only object which are marked as published
    event_submissions = CalendarSubmission.objects.filter(published=True)
    return render(request, 'event_submission_list.html', {'event_submissions': event_submissions})