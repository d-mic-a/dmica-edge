from django.urls import path
from .views import dmicaedge

urlpatterns = [
    path('prediction/', HandPredictions.as_view(), name='HandPredictions'),
    path('mic_control/', MicControl.as_view(), name='MicControl'),
]
