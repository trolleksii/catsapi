from django.urls import re_path

from .views import CatAPIView

urlpatterns = [
    re_path('', CatAPIView.as_view(), name='catapi_view'),
]
