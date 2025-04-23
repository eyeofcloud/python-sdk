import json,logging,requests
from requests import exceptions as request_exception
from.helpers import enums
REQUEST_TIMEOUT=10
class EventDispatcher:
	@staticmethod
	def dispatch_event(event):
		' Dispatch the event being represented by the Event object.\n\n    Args:\n      event: Object holding information about the request to be dispatched to the Eyeofcloud backend.\n    ';A=event
		try:
			if A.http_verb==enums.HTTPVerbs.GET:requests.get(A.url,params=A.params,timeout=REQUEST_TIMEOUT).raise_for_status()
			elif A.http_verb==enums.HTTPVerbs.POST:requests.post(A.url,data=json.dumps(A.params),headers=A.headers,timeout=REQUEST_TIMEOUT).raise_for_status()
		except request_exception.RequestException as B:logging.error('Dispatch event failed. Error: %s'%str(B))