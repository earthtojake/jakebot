import os.path
import sys
import json
import apiai
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ACCESS_TOKEN = '91c67ef0b7c847be8f1e6fd64bbf761a'
DEV_ACCESS_TOKEN = 'c7d3d04b092445639ba0e3fda70d82da'

hdr = {
	"Content-Type": "application/json; charset=utf-8",
	"Authorization": "Bearer c7d3d04b092445639ba0e3fda70d82da"
}

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def respond(senderId,message):

	request = ai.text_request(sessionId=senderId)

	request.query = message

	response = json.loads(request.getresponse().read())

	if response.get('status').get('code') != 200:
		print 'Error',response.get('status')
		return None
	else:
		text = response.get('result').get('fulfillment').get('speech')
		return text

def create_intent(iID,inputs,response,context=False):

	userSays = []
	if type(inputs) is not list: inputs = [inputs]
	for text in inputs:
		userSays.append({
				"data": [{"text": text}],
				"isTemplate": False,
				"count": 0
			})

	intent = {
		"name": iID,
		"auto": True,
		"contexts": [],
		"userSays": userSays,
		"responses": [
			{
				"affectedContexts": [{"name": iID,"lifespan": 5}],
				"resetContexts": False,
				"speech": response
			}
		],
	   "priority": 500000
	}

	return requests.post('https://api.api.ai/v1/intents?v=20150910',data=json.dumps(intent),headers=hdr)

def test():
	while True:
		message = raw_input("User: ")
		print 'Bot:',respond(message)