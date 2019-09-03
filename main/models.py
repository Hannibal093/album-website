from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from uuid import uuid4
import os

# Create your models here.

class category(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)

	class Meta:
		verbose_name_plural = "Categories"
	
	def __str__(self):
		return self.title
		
class album(models.Model):
	title = models.CharField(max_length=200)
	published = models.DateTimeField("date published", default=datetime.now())
	summary = models.CharField(max_length=200)
	
	slug = models.CharField(max_length=200)
	user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
	class Meta:
		verbose_name_plural = "Albums"
	
	def __str__(self):
		return self.title
	
	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)

def content_file_name(instance, filename):
	
	return '/'.join(['images', instance.user.username, filename])

class photo(models.Model):
	filename = models.CharField(max_length=100, default= uuid4().hex + '.jpg')
	published = models.DateTimeField("date published", default=datetime.now())
	user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
	content = models.FileField(upload_to=content_file_name)
	albums = models.ForeignKey(album, default=1, on_delete=models.SET_DEFAULT)

	def delete(self, *args, **kwargs):
		self.content.delete()
		super().delete(*args, **kwargs)

