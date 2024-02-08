# ps_submission/urls.py
from django.urls import path
from .views import exhibition_submission_create, exhibition_list, exhibition_submission_detail

urlpatterns = [
    path('submit', exhibition_submission_create, name='exhibition_submission_create'),
    path('', exhibition_list, name='exhibition_list'),
    path('<int:submission_id>-<slug:submission_project_title>/', exhibition_submission_detail, name='exhibition_submission_detail'),
    # Add more patterns as needed
]
