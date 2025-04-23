class LogEvent:
	' Representation of an event which can be sent to Eyeofcloud events API. '
	def __init__(A,url,params,http_verb=None,headers=None):A.url=url;A.params=params;A.http_verb=http_verb or'POST';A.headers=headers
	def __str__(A):return str(A.__class__)+': '+str(A.__dict__)