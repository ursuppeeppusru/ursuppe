# ps_pinboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.utils import timezone

from .forms import PinboardForm
from .models import PinBoard


def today():
    today = timezone.now().date()
    return today

def pinboard_post(request):
    if request.method == 'POST':
        pinboard_form = PinboardForm(request.POST)

        if pinboard_form.is_valid():
            post = pinboard_form.save()

            # Add more logic here if needed, such as redirecting to a success page.
            messages.success(request,
                             "Thank you for adding your post. We will look it through shortly.")
            return redirect('/pinboard/post')
        else:
            messages.error(request, "Some error occurred while submitting. Please re-check your form.")
    else:
        pinboard_post = PinboardForm()

    return render(request, 'pinboard_form.html', {
        'pinboard_post': pinboard_post,
    })


@cache_page(60 * 60)
def pinboard_list(request):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    pinboard_posts = PinBoard.objects.filter(published=True)
    pinboard_categories = PinBoard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_list.html',
                  {'today': today, 'pinboard_posts': pinboard_posts, 'pinboard_categories': pinboard_categories})

@cache_page(60 * 60)
def pinboard_list_category(request, category):
    # Only objects which are marked as published, where end date has not exceeded and opening date has started
    pinboard_posts = PinBoard.objects.filter(category=category).filter(published=True)
    pinboard_categories = PinBoard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_list.html',
                  {'today': today, 'pinboard_posts': pinboard_posts, 'pinboard_categories': pinboard_categories})

@cache_page(60 * 60)
def pinboard_detail(request, post_id):
    post = get_object_or_404(PinBoard, id=post_id)
    pinboard_categories = PinBoard.objects.values_list('category', flat=True).distinct()
    return render(request, 'pinboard_detail.html', {'today': today, 'post': post, 'pinboard_categories': pinboard_categories})