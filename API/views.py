from API.models import *
from django.utils import simplejson
import datetime
from bs4 import BeautifulSoup
import urllib
from time import strptime
from django.http import HttpResponse
from util import cHttpResponse
import math

def getEvents(request, year, month, day):
	date_string = year+month+day
	date_search_query = datetime.datetime.strptime(date_string, '%Y%m%d').date()
	event_for_day = Event.objects.filter(date=date_search_query).order_by('-going_count')
	event_list = []
	for event in event_for_day:
		date_fix = event.date.strftime('%m/%d/%Y')
		time_fix = event.time.strftime('%H:%M:%S')
		event_dict = {'identifier': event.pk, 'title': event.title, 'description': event.description, 'time': time_fix, 'date': date_fix, 'address': event.address}
		event_list.append(event_dict)
	json_returned = simplejson.dumps(event_list)
	return cHttpResponse(json_returned)

def getEventsWithDateRange(request, year, month, day, year1, month1, day1):
	date_string = year+'-'+month+'-'+day
	date_string1 = year1+'-'+month1+'-'+day1

	event_for_day = Event.objects.filter(date__range=[date_string, date_string1]).order_by('-going_count')
	event_list = []
	for event in event_for_day:
		date_fix = event.date.strftime('%m/%d/%Y')
		time_fix = event.time.strftime('%H:%M:%S')
		event_dict = {'identifier': event.pk, 'title': event.title, 'description': event.description, 'time': time_fix, 'date': date_fix, 'address': event.address}
		event_list.append(event_dict)
	json_returned = simplejson.dumps(event_list)
	return cHttpResponse(json_returned)

def getEvent(request, identifier):
	event = Event.objects.get(pk=identifier)
	date_fix = event.date.strftime('%m/%d/%Y')
	time_fix = event.time.strftime('%H:%M:%S')
	event_dict = {'identifier': event.pk, 'title': event.title, 'description': event.description, 'time': time_fix, 'date': date_fix, 'address': event.address, 'org': event.org, 'going_count': event.going_count, 'hashtag': event.hashtag}
	json_returned = simplejson.dumps(event_dict)
	return cHttpResponse(json_returned)

def scrapeCalendars(request):
	def clean_whitespace(s) :
		return ' '.join(s.split())

	base_url = "http://visitlongmont.org/event/?p=%s"
	page = 1
	run = True
	while run == True:
		page_source = urllib.urlopen(base_url % (page)).read()
		soup = BeautifulSoup(page_source, "html5lib")
		amount = soup.find("p", class_="amount").contents
		amount = clean_whitespace(amount[0]).split(' ')

		num_pages = math.ceil(int(amount[5]) / 8)

		if page < num_pages:
			events = soup.find_all("div", class_="result-details-wrapper")

			dates = []
			for event in events:
				eventdate = event.select(".date")
				eventdate = eventdate[0].contents
				date_s = eventdate[0]
				date_s = date_s[:-3]

				date_a = []
				date_a = date_s.split(' ')
				month_number = strptime(date_a[1], '%b').tm_mon
				day = int(date_a[0])
				year = int(date_a[2])
				date_obj = datetime.date(year, month_number, day)
				time_obj = datetime.datetime.time(datetime.datetime.now())

				title = event.select(".title")
				title_link = title[0].find_all('a')
				title = title_link[0].contents
				title = clean_whitespace(title[0])

				line_containers = event.select(".line-container")

				description = line_containers[1].p
				full_description_link = description.find_all('a');
				if len(full_description_link) != 0:
					url = full_description_link[0]['href']
					page_source = urllib.urlopen(url).read();
					soup = BeautifulSoup(page_source, "html5lib")

					inner_line_containers = soup.find_all("div", class_="line-container")
					description = inner_line_containers[5].contents
				else:
					description = description.contents

				description = clean_whitespace(description[0])

				address = line_containers[0].div.contents
				address = clean_whitespace(address[0] + ' ' + address[2])


				new_event = Event.objects.create(title=title, date=date_obj, time=time_obj, description=description, address=address)
				new_event.save()
		else:
			run = False
		page += 1

	return HttpResponse(dates)

def processImGoing(request, identifier):
	event = Event.objects.get(pk=identifier)
	event.going_count += 1
	event.save()

	json = {'status': 'done'}
	json_returned = simplejson.dumps(json)

	return cHttpResponse(json_returned)
