from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.models import Query

from django.db.models import Q

from ps_submission.models import ExhibitionSubmission
from ps_calendar.models import CalendarSubmission

def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        
        archive_results = ExhibitionSubmission.objects.filter(Q(project_title__icontains=search_query) | Q(subtitle__icontains=search_query) | Q(artists__icontains=search_query) | Q(curators__icontains=search_query) | Q(location__icontains=search_query) | Q(photographer__icontains=search_query)).order_by('-exhibition_end')
        events_results = CalendarSubmission.objects.filter(Q(project_title__icontains=search_query) | Q(subtitle__icontains=search_query) | Q(artists__icontains=search_query) | Q(curators__icontains=search_query) | Q(location__icontains=search_query)).order_by('-exhibition_opening')
        search_results = Page.objects.live().search(search_query)
        
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()
        archive_results = ExhibitionSubmission.objects.none()
        events_results = CalendarSubmission.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "archive_results": archive_results,
            "events_results": events_results,
        },
    )
