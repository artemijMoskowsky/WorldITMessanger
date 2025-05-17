from django.urls import path
from .views import CoreView, MyPublicationsView


urlpatterns = [
    path('', CoreView.as_view(), name='core'),
    path('my_publications/', MyPublicationsView.as_view(), name='my_publications'),
]
