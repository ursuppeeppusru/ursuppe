# ps_pinboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone

from .forms import PinboardForm, PinboardImagesForm
from .models import Pinboard, PinboardImages


def today():
    today = timezone.now().date()
    return today

def pinboard_post(request):
    ImageFormSet = modelformset_factory(PinboardImages, form=PinboardImagesForm, extra=1)

    if request.method == 'POST':
        pinboard_form = PinboardForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=PinboardImages.objects.none())

        if pinboard_form.is_valid() and formset.is_valid():
            post = pinboard_form.save()
            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.pinboard = post
                    image.save()

            # Add more logic here if needed, such as redirecting to a success page.
            messages.success(request,
                             "Thank you for adding your post. We will look it through shortly.")
            return redirect('/pinboard/post')
        else:
            messages.error(request, "Some error occurred while submitting. Please re-check your form.")
    else:
        pinboard_post = PinboardForm()
        formset = ImageFormSet(queryset=PinboardImages.objects.none())

    return render(request, 'pinboard_form.html', {
        'pinboard_post': pinboard_post,
        'formset': formset,
    })

@cache_page(60 * 60)
def pinboard_list(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    pinboard_posts = Pinboard.objects.filter(published=True).order_by('-created_at')
    pinboard_categories = Pinboard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_list.html',
                  {'today': today, 'pinboard_posts': pinboard_posts, 'pinboard_categories': pinboard_categories})

@cache_page(60 * 60)
def pinboard_list_category(request, category):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    pinboard_posts = Pinboard.objects.filter(category=category).filter(published=True).order_by('-created_at')
    pinboard_categories = Pinboard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_list.html',
                  {'today': today, 'pinboard_posts': pinboard_posts, 'pinboard_categories': pinboard_categories})

@cache_page(60 * 60)
def pinboard_detail(request, post_id):
    post = get_object_or_404(Pinboard, id=post_id)
    pinboard_categories = Pinboard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_detail.html', {'today': today, 'post': post, 'pinboard_categories': pinboard_categories})