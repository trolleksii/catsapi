from django.urls import path

from catapi.settings import SITE_URL

from .views import BreedsView, IndexView, SpecsView

app_name = 'ui'

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('breeds', BreedsView.as_view(), name='breeds_page'),
    path('specs', SpecsView.as_view(), {'site_url': SITE_URL}, name='specs_page'),
]
