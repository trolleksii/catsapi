from django.urls import path

from .views import BreedsView, IndexView, SpecsView

app_name = 'ui'

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('breeds', BreedsView.as_view(), name='breeds_page'),
    path('specs', SpecsView.as_view(), name='specs_page'),
]
