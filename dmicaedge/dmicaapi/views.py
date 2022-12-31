import numpy as np
import pandas as pd
# from .apps import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
# import urllib # python 2
import urllib.request # python 3
import json
import os
import sys 
print(sys.path)
sys.path.append('/home/fog-server/dmica/dmica-edge/dmicaedge')
from backend.model.yolov7PoseEstimation.poseEstimate import detect


# import sys 
# sys.path.append('../dmicaedge')
# from dmicaedge.backend.model.yolov7-pose-estimation.pose-estimate import detect

# Create your views here.


def detect(request):
    data = {"success": False}
    
    if request.method == "POST":
        if request.FILES.get("image",None) is not None:
            image = _grab_image(stream=request.FILES["image"])
        else:
            url = request.POST.get("url", None)
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)
            image = _grab_image(url=url)
    
def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)
	# otherwise, the image does not reside on disk
	else:	
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.request.urlopen(url)
			data = resp.read()
		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()
		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image




'''
class RequesterAction(APIView):
    def post(self, request):
        #data = request.data
        print(0000000000000000000)
        print('before get image')
        image_data = request.GET.get('image')
        print('after get image')
        image_shape = request.GET.get('shape')
        #detection_model = AppConfig.models
        print(image_data)
        input()
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
        
        
'''
        