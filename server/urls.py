"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from server.server import *
from django.conf.urls import url, include
#from django.conf.urls import patterns
from django.contrib import admin
#from mysite.main import index
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
import jieba, sqlite3, pickle, re
from audiotranscode import _filetype
from audiotranscode import *
at = AudioTranscode()
@csrf_exempt
def index(request):
	return HttpResponse('hello world')

@csrf_exempt
def photo(request):
	image = request.body
	print(len(image))
	for i in range(400):
		if image[i:i+4] == b'\r\n\r\n':
			image = image[i+4:]
			break
	for i in range(len(image)-2, len(image)-100, -1):
		if image[i-1:i+1] == b'\r\n':
			image = image[:i-1]
			break
	print(len(image))
	str_des = get_description(image, 1)
	str_ocr = ocr(image)
	print('返回文字：\n' + str_des + '\n' + str_ocr + '\n')
	return HttpResponse(str_des + '\n' + str_ocr)

@csrf_exempt
def audio(request):
	print(request)
	au = request.body
#print('au=', au)
	f = open('audio.wav', 'wb')
	f.write(au)
	f.close()
	at.transcode('audio.wav', 'audio1.wav')
	f = open('audio1.wav', 'rb')
	all_data = f.read()
	for i in range(len(all_data)):
		if all_data[i:i+4] == b'\r\n\r\n':
			all_data = all_data[i+4:]
			break
	print(all_data[:100], all_data[-100:])
	f.close()
	return HttpResponse(get_words(all_data))

@csrf_exempt
def config(request):
	set_config(request.POST)
	return HttpResponse('')

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', index),
	url(r'^photo', photo),
	url(r'^audio', audio),
	url(r'^config', config),
]
