# ps_submission/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from django.views.decorators.cache import cache_page

from .forms import ExhibitionSubmissionForm, ExhibitionImagesForm
from .models import ExhibitionImages, ExhibitionSubmission


def exhibition_submission_create(request):
    errors = None
    if request.method == 'POST':
        submission_form = ExhibitionSubmissionForm(request.POST)
        ImageFormSet = modelformset_factory(ExhibitionImages, form=ExhibitionImagesForm)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ExhibitionImages.objects.none())

        if submission_form.is_valid() and formset.is_valid():
            if 5 <= formset.total_form_count() <= 21:
                submission = submission_form.save()
                for form in formset:
                    if form.cleaned_data:
                        image = form.save(commit=False)
                        image.activity = submission
                        image.save()

                messages.success(request, "Thank you for creating your archive. We will look through your submission shortly, and if it meets our criteria it will be published onto this platform. By creating your archive you have also accepted the possibility of being featured on the index page highlighted by our board of artist-moderators, as well as on our social media.")
                return redirect('/archive/create')
            else:
                messages.error(request, "There must be a minimum of 5 images and a maximum 20 images. Please re-submit the form.")
        else:
            
            # print(formset.errors)
            errors = {}
            for error_dict in formset.errors:
                if error_dict:
                    for key, value in error_dict.items():
                        #if isinstance(value, str) or key == 'image':
                        errors[key.upper()] = value[0].upper()
            
            #errors = formset.errors
            
            messages.error(request, "Some error occurred. Please re-check and re-submit the form.")
            formset = ImageFormSet(queryset=ExhibitionImages.objects.none())
            
    else:
        submission_form = ExhibitionSubmissionForm()
        ImageFormSet = modelformset_factory(ExhibitionImages, form=ExhibitionImagesForm)
        formset = ImageFormSet(queryset=ExhibitionImages.objects.none())

    return render(request, 'exhibition_submission_form.html', {
        'submission_form': submission_form,
        'formset': formset,
        'errors': errors
    })

@cache_page(60 * 60)
def exhibition_list(request):
    # Only object which are marked as published
    submissions = ExhibitionSubmission.objects.filter(published=True).order_by('-exhibition_end')

    # Get unique years and pass to template
    years = ExhibitionSubmission.objects.filter(published=True).values_list('exhibition_opening__year', flat=True).distinct()

    return render(request, 'submission_list.html', {'submissions': submissions, 'years': years})

@cache_page(60 * 60)
def exhibition_list_year(request, year):
    # Only object which are marked as published sorted by year
    submissions = ExhibitionSubmission.objects.filter(published=True, exhibition_opening__year=year).order_by('-exhibition_end')

    # Get unique years and pass to template
    years = ExhibitionSubmission.objects.filter(published=True).values_list('exhibition_opening__year', flat=True).distinct()

    return render(request, 'submission_list.html', {'submissions': submissions, 'years': years})

@cache_page(60 * 60)
def exhibition_submission_detail(request, submission_id, submission_project_title):
    submission = get_object_or_404(ExhibitionSubmission, id=submission_id)
    return render(request, 'exhibition_submission_detail.html', {'submission': submission})
