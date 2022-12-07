import numpy as np
import pandas as pd
from .apps import AppConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
class HandPredictions(APIView):
    def post(self, request):
        data = request.image
        
        #information for processing changes by the image classification module
        if data == None :
            pass
        else :
            pass
        
        prediction_model = AppConfig.model
        prediction_result = prediction_model.predict()
        response_data = prediction_result
        return Response(response_data, status=200)
    
class MicControl(APIView):
    def post(self, request):
        data = request.image
        
        data = request.image
        
        #information for processing changes by the image classification module
        if data == None :
            pass
        else :
            pass
        
        prediction_model = AppConfig.model
        prediction_result = prediction_model.predict()
        response_data = prediction_result
        return Response(response_data, status=200)
        
        
        
        