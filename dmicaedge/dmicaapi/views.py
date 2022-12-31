import numpy as np
import pandas as pd
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
import sys 
print(sys.path)
sys.path.append('/home/fog-server/dmica/dmica-edge')
from dmicaedge.backend.model.yolov7PoseEstimation.poseEstimate import detect


# import sys 
# sys.path.append('../dmicaedge')
# from dmicaedge.backend.model.yolov7-pose-estimation.pose-estimate import detect

# Create your views here.
class RequesterAction(APIView):
    def post(self, request):
        #data = request.data
        image_data = request.GET.get('image')
        image_shape = request.GET.get('shape')
        detection_model = AppConfig.models
        data = [image_data, image_shape]
        detect(image_data)
        return HttpResponse(data)
        # return image_data, image_shape
        
        # predicting the raise hand
        prediction_hand = detection_model([[image_data, image_shape]])
        response_hand = {prediction_hand}
        print(response_hand)
        return Response(response_hand,status=200)
    
class VigilantInformation(APIView):
    def post(self, request):
        data = request.data
        
        #information for processing  the data post by client side
        
        # return Response(response_data, status=200)
    
class ObservantControl(APIView):
    def post(self, request):
        data = request.data
        
        #information for processing the data post by client side
        if data == None :
            pass
        else :
            pass
   
        # return Response(response_data, status=200)
    
class ObservantInformation(APIView):
    def post(self, request):
        data = request.data
        
        #information for processing changes by the image classification module
        if data == None :
            pass
        else :
            pass
       
        # return Response(response_data, status=200)
        
        
        
        