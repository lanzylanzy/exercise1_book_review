from django.urls import path
from backend.views import db_info_view, debug_douban_raw, gr_info_view
from django.http import JsonResponse  # ✅ 引入 JsonResponse 响应类

urlpatterns = [
    path('', lambda request: JsonResponse({'status': 'ok'})),
    path('debug/douban-raw/', debug_douban_raw),
    path('book/db/', db_info_view),         # /api/book/?q=xxx
    path('book/gr/', gr_info_view),  # /api/book/status/?isbn=xxx
]

#python manage.py runserver




