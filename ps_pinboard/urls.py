# ps_pinboard/urls.py
from django.urls import path
from .views import pinboard_list, pinboard_list_category, pinboard_post, pinboard_detail

urlpatterns = [
    path('', pinboard_list, name='pinboard_list'),
    path('category/<str:category>/', pinboard_list_category, name='pinboard_list_category'),
    path('post', pinboard_post, name='pinboard_post'),
    path('<int:post_id>/', pinboard_detail, name='pinboard_detail'),
    # Add more patterns as needed
]
