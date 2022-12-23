from django.apps import AppConfig
import os
import joblib
from django.conf import settings


class DmicaapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dmicaapi'
    MODEL_FIlE = os.path.join(settings.MODELS, "PoseEstimate.joblib")
    model =joblib.load(MODEL_FIlE)