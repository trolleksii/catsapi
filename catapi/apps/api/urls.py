from django.urls import re_path

from .views import AllCatsAPIView, BreedAPIView, CatAPIView, RandomCatAPIView

app_name = 'api'


urlpatterns = [
    re_path(r'^all$', AllCatsAPIView.as_view(), name='list_all_cats'),
    re_path(r'^random$', RandomCatAPIView.as_view(), name='get_random'),
    re_path(r'^breeds$', BreedAPIView.as_view(), name='list_create_breed'),
    re_path(r'^breeds/(?P<breed_slug>[\w\-]+)$', CatAPIView.as_view(), name='list_create_cat'),
    re_path(r'^breeds/(?P<breed_slug>[\w\-]+)/random$', RandomCatAPIView.as_view(), name='get_random_of_breed'),
]
