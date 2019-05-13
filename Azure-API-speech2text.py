#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import requests
import json
import base64
import fleep
from datetime import datetime
from datetime import date
import re
app = Flask(__name__)



subscription_key = 'cf9730a166574bc184bd14f5a73f4616'


def get_token(subscription_key):
	fetch_token_url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
	headers = {
		'Ocp-Apim-Subscription-Key': subscription_key
	}
	response = requests.post(fetch_token_url, headers=headers)
	access_token = str(response.text)
	#print(access_token)
	return access_token


def get_text(data):


	file_info = fleep.get(data)
	print(file_info.extension[0])
	print(file_info.extension[0]=='wav')

	if(file_info.extension[0]=='wav'):
		TYPE = 'audio/wav; codecs=audio/pcm; samplerate=16000'
	else:
		TYPE = 'audio/ogg; codecs=opus'

	Bearer = get_token(subscription_key)
	url = 'https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed'
	headers = {
		'Ocp-Apim-Subscription-Key': subscription_key,
		'Authorization': Bearer,
		'Content-type': TYPE,
		'Accept': 'application/json'
	}

	response = requests.post(url, headers=headers,data=data)

	return response	



@app.route('/', methods=['GET', 'POST'])
def index():
	if (request.method == 'POST'):

		try:
			headers = request.headers
			data = base64.b64decode(request.data)
			res = get_text(data)
			return jsonify(res.json())
				
		except Exception as e:
			print(e)

		return ({"result": "Error, plz check log"})

	else:
		return jsonify({"result": "POST requests only"})


if __name__ == '__main__':
	app.run(debug=True)