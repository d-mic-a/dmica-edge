import numpy as np
import pandas as pd
from .apps import AppConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

import sys 
sys.path.append("..")
from backend.model.yolov7-pose-estimation.pose-estimate import detect

# Create your views here.
class RequesterAction(APIView):
    def post(self, request):
        data = request.image
        
        #information for processing changes by the image classification module
        if data == None :
            pass
        else :
            pass
        
        ret = detect(data)
        # ret will be 'None' if no one start or stop in this image 
        # ret[0] is [x, y, z]
        # ret[1] is 'left' or 'right' 
        return Response(ret, status=200)
    
class VigilantInformation(APIView):
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
    
class ObservantControl(APIView):
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
    
class ObservantInformation(APIView):
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
        
        
        
        