from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from ps_submission import urls as exhibition_urls
from ps_calendar import urls as calendar_urls
from ps_list import urls as list_urls
from ps_calendar_subscription import urls as events_subscription_urls
from ps_pinboard import urls as pinboard_urls

from search import views as search_views

from .views import highlights

urlpatterns = [
    path('', highlights, name="highlights"),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('archive/', include(exhibition_urls)),
    path('events/', include(calendar_urls)),
    path('feed/', include(events_subscription_urls)),
    path('list/', include(list_urls)),
    path('pinboard/', include(pinboard_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
