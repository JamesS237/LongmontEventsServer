from django.db import models

class Event(models.Model):
	title = models.CharField(max_length=70, default="Unknown")
	description = models.CharField(max_length=300, default="Unknown")
	time = models.TimeField(default=None)
	date = models.DateField(default=None)
	address = models.CharField(max_length=100, default="Unknown")
	org = models.CharField(max_length=50, default="Unknown")
	going_count = models.IntegerField(default=0)
	hashtag = models.CharField(max_length=25, default="Longmont")

	def __unicode__(self):
		return self.title