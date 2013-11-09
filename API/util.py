from django.http import HttpResponse

def cHttpResponse(string):
	response = HttpResponse(string)
	response['Access-Control-Allow-Origin'] = '*'
	return response