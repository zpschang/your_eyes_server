
# coding: utf-8

# In[1]:
import requests

last_image = ''
# In[2]:

import json
def get_description(image, num):
	global last_image
	last_image = image
	headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': 'b33a4dd9d5a1430293b56028b2d5bd15'}
	response = requests.post('https://api.projectoxford.ai/vision/v1.0/describe?maxCandidates=%d' % num, 
							 data=image, headers=headers)
	d = response.json()
	print(d)
	try:
		return d['description']['captions'][num-1]['text']
	except:
		return 'fail'


# In[3]:

f = open('/Users/pushi/Desktop/WechatIMG5.jpeg', 'rb')


# In[4]:

image = f.read()


# In[5]:

#print(get_description(image, 1))


# In[6]:
jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzY29wZSI6Imh0dHBzOi8vc3BlZWNoLnBsYXRmb3JtLmJpbmcuY29tIiwic3Vic2NyaXB0aW9uLWlkIjoiODNlZDA1MTZlYTliNGIwMWJhMmMyZTBkYmE0ZDc1ZmIiLCJwcm9kdWN0LWlkIjoiQmluZy5TcGVlY2guUHJldmlldyIsImNvZ25pdGl2ZS1zZXJ2aWNlcy1lbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNvZ25pdGl2ZS5taWNyb3NvZnQuY29tL2ludGVybmFsL3YxLjAvIiwiYXp1cmUtcmVzb3VyY2UtaWQiOiIiLCJpc3MiOiJ1cm46bXMuY29nbml0aXZlc2VydmljZXMiLCJhdWQiOiJ1cm46bXMuc3BlZWNoIiwiZXhwIjoxNDc2NTM3Mjg1fQ.akpxhI6tN_NWULJkMsmBxlgKEWKZ5S_hc2jq7_bbE9o'

def get_words(wav):
	"""headers = {'Content-Type': 'audio/wav; samplerate=16000',
		'Ocp-Apim-Subscription-Key': '3970e3ce4f51493f92a4c5f0c7904ed1',
		'Authorization': 'Bearer %s' % jwt_token
	}
	response = requests.post('speech.platform.bing.com/recognize?scenarios=catsearch&appid=f84e364c-ec34-4773-a783-73707bd9a585&locale=zh-CN&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66', 
							 data=wav, headers=headers)
	d = response.json()
	sentence = d['results']['name']
	return sentence
	sentence = '帮助我' #aaaa
	jieba.split()
	"""
	s = requests.session()
	s.auth = ('4eca10fc-dda0-4d80-aaca-726f434d4b79', 'scXAdLTlODwp')
	headers = {'Content-Type':'audio/wav'}
	response = s.post('https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?timestamps=true&word_alternatives_threshold=0.9&continuous=true&model=zh-CN_BroadbandModel',
			data=wav, headers=headers)
	d = response.json()
	print('json:  ', d, '\n\n\n')
	str = ''
	word_list = []
	for i in d['results'][0]['alternatives'][0]['timestamps']:
		word_list.append(i[0])
	str = d['results'][0]['alternatives'][0]['transcript']
	print('str=', str)
	maxi_op = 0
	choose_op = None
	for op in oper_list:
		maxi = 0
		for word in word_list:
			try:
				simi = model_ch.similarity(word, op.name)
			except:
				simi = 0
			if simi > maxi:
				maxi = simi
		if maxi > maxi_op:
			maxi_op = maxi
			choose_op = op
		print(op.name, maxi)
	print('maxi_op=', maxi_op)
	str = choose_op.str + '\n'
	str += choose_op.func()
	print(str)
	return str

# In[7]:

import re
def ocr(image):
	global last_image
	last_image = image
	headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': 'b33a4dd9d5a1430293b56028b2d5bd15'}
	response = requests.post('https://api.projectoxford.ai/vision/v1.0/ocr?detectOrientation=true',
							data=image, headers=headers)
	d = response.json()
	str = ''
	print(d)
	if d['orientation'] != 'NotDetected':
		str += '检测到文字：\n'
		for region in d['regions']:
			for line in region['lines']:
				for word in line['words']:
					str += word['text']
					match = re.search('[a-zA-Z]', word['text'])
					if match:
						str += ' '
				str += '\n'
	"""headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Ocp-Apim-Subscription-Key':
	'90795f500c6d436c99e6fd099e3848ae'}
	response = requests.post('https://api.cognitive.microsoft.com/bing/v5.0/spellcheck/?mode=proof',
			data='Text='+str, headers=headers)
	print(response.json())
	"""
	"""
	str = ''
	response = requests.post('https://api.projectoxford.ai/vision/v1.0/ocr?language=%s&detectOrientation=true' % 'en',
							data=image, headers=headers)
	d = response.json()
	
	if d['orientation'] != 'NotDetected':
		for region in d['regions']:
			for line in region['lines']:
				for word in line['words']:
					str1 += word['text'] + ' '
				str1 += '\n'
	"""
	return str

# In[8]:

#ocr(image)


# In[9]:

import http.client, urllib.parse, json
def get_wave(string, lang):
	#Note: The way to get api key:
	#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
	#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
	apiKey = "3970e3ce4f51493f92a4c5f0c7904ed1"

	params = ""
	headers = {"Ocp-Apim-Subscription-Key": apiKey}

	#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
	AccessTokenHost = "api.cognitive.microsoft.com"
	path = "/sts/v1.0/issueToken"

	# Connect to server to get the Access Token
	print ("Connect to server to get the Access Token")
	conn = http.client.HTTPSConnection(AccessTokenHost)
	conn.request("POST", path, params, headers)
	response = conn.getresponse()
	print(response.status, response.reason)

	data = response.read()
	conn.close()

	accesstoken = data.decode("UTF-8")
	print ("Access Token: " + accesstoken)

	body = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>%s</voice></speak>" % string

	headers = {"Content-type": "application/ssml+xml", 
				"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
				"Authorization": "Bearer " + accesstoken, 
				"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
				"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
				"User-Agent": "TTSForPython"}

	#Connect to server to synthesize the wave
	print ("\nConnect to server to synthesize the wave")
	conn = http.client.HTTPSConnection("speech.platform.bing.com")
	conn.request("POST", "/synthesize", body, headers)
	response = conn.getresponse()
	print(response.status, response.reason)

	data = response.read()
	conn.close()
	print("The synthesized wave length: %d" %(len(data)))


# In[10]:

class oper:
	def __init__(self, func, name, str):
		self.func = func
		self.name = name
		self.str = str


# In[11]:

oper_list = []
def func_help():
	str = '可用的操作有：\n'
	for oper in oper_list:
		str += oper.str + '\n'
	return str
oper_list.append(oper(func_help, '帮助', '获得帮助'))

def func_weather():
	str = ''
	str = '获得天气的功能还在开发中'
	return str
oper_list.append(oper(func_weather, '天气', '获得天气'))

def func_object():
	headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': 'b33a4dd9d5a1430293b56028b2d5bd15'}
	response = requests.post('https://api.projectoxford.ai/vision/v1.0/describe', 
							 data=last_image, headers=headers)
	d = response.json()
	str = ''
	try:
		for word in d['description']['tags']:
			str += word + '\n'
	except:
		pass
	return str

oper_list.append(oper(func_object, '物体', '描述周围物体'))
# In[12]:

oper_list[0].func()


# In[13]:

# import modules & set up logging
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
sentences = [['first', 'sentence'], ['second', 'sentence']]
# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)


# In[28]:

import os
import jieba

def cal_model():
	global model_ch, model_en
	try:
		model_ch = gensim.models.Word2Vec.load('model_ch')
		model_en = gensim.models.Word2Vec.load('model_en')
		return
	except: pass
	sentences = []
	s = 0
	for d in os.listdir('/Users/pushi/mysite/html'):
		article = open('/Users/pushi/mysite/html/'+d, 'rb').read()
		sentence = []
		for word in jieba.cut(article):
			sentence.append(word)
			if word == '。':
				sentences.append(sentence)
				sentence = []
		s += 1
		if s % 500 == 0:
			print(s)
	model_ch = gensim.models.Word2Vec(sentences)


# In[44]:

	text = open('/Users/pushi/Downloads/text8').read()


# In[48]:

	text[:100]


# In[49]:

	sentences = gensim.models.word2vec.Text8Corpus('/Users/pushi/Downloads/text8')


# In[50]:

	model_en = gensim.models.Word2Vec(sentences, size=200)


# In[51]:

	model_en.similarity('woman', 'man')


# In[52]:



# In[ ]:


	model_ch.save('model_ch')
	model_en.save('model_en')

cal_model()

def set_config(_config):
	global config
	config = _config

