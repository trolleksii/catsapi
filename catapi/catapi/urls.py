from django.urls import include, path

urlpatterns = [
    path('', include('apps.ui.urls')),
    path('api/', include('apps.api.urls'))
]
