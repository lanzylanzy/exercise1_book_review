from django.urls import path
from backend.views import db_info_view, gr_info_view

urlpatterns = [
    path('book/db/', db_info_view),         # /api/book/?q=xxx
    path('book/gr/', gr_info_view),  # /api/book/status/?isbn=xxx
]

#python manage.py runserver