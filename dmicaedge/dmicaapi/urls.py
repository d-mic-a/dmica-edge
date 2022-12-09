from django.urls import path
from .views import *

urlpatterns = [
    path('requester_action/', RequesterAction.as_view(), name='RequesterAction'),
    path('vigilant_information', VigilantInformation.as_view(), name='VigilantInformation'),
    path('observant_control/', ObservantControl.as_view(), name='ObservantControl'),
    path('observant_information', ObservantInformation.as_view(), name='ObservantInformation'),
]
