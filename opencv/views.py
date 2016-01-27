from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from urlparse import urlparse, parse_qs

import sys
import numpy as np
import cv2
import json

class Components:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

def index(request):
    components = []
    ret = ''
    qs = parse_qs(request.GET.urlencode())
    if qs.has_key('q'):
        try:
            scale = 2
            neighbor = 20
            iw = 50
            ih = 50
            q = qs['q'][0].encode('utf-8')
	    ok_cascade = cv2.CascadeClassifier('/root/Training/classifier-very-good/cascade.xml')
            img = cv2.imread(q)
            size = (iw, ih)
            count = 0
            img = cv2.resize(img, (800, 600));
            oks = ok_cascade.detectMultiScale(img, scaleFactor=scale, minNeighbors=neighbor, minSize=size, flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            for (x, y, w, h) in oks:
              cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
              component = Components(x, y, w, h)
              if (count != 0):
                ret += ','
              count += 1
              ret += '{\"type\":\"button\",\"text\":\"OK\",\"x\":'+ str(x) + ',\"y\":' + str(y) + ',\"width\":' + str(w) +',\"height\":' + str(h) + '}'
              #return JsonResponse(component, safe=False)
              #return HttpResponse(json.dumps(component), safe=False)
              #return JsonResponse({'foo':'bar'})              
              #return HttpResponse(json.dumps(component, default=lambda o: o.__dict__, sort_keys=True, indent=0))
              # return HttpResponse(ret)
              components.append(component)
            
            cv2.imwrite('/root/simple/recent.jpg', img)
            return HttpResponse('{\"components\":[' + ret + ']}')
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # return JsonResponse();
        except Exception as e:
            rri = 1
            return HttpResponse('Unexpected error: ' + e.message)

	# TODO: Check path for security
        
#	return  HttpResponse('{\"components\":[{\"type\": \"Button\",\"x\": 0,\"y\": 0,\"width\": 100,\"height\":40},{\"type\": \"Button\",\"x\": 100,\"y\": 40,\"width\": 200,\"height\": 50}]}')
        #return HttpResponse('OpenCV: ' + cv2.__version__ + q + str(img))
    else:
        return HttpResponse('Missing required query string \'q\'');
