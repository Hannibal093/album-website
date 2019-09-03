from django import forms
from .models import photo, album
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField
from uuid import uuid4

def rename(filename):
	filename = replace_space(filename)
	ext = filename.split('.')[-1]
	original = filename.split('.')[0]
	filename = '{}_{}.{}'.format(original, uuid4().hex, ext)
	return filename

def replace_space(somewords):
    return str(somewords).replace(" ","-",-1)

class photoform(forms.ModelForm):
	
	attachments = MultiFileField(min_num=1, max_num=10, max_file_size=2048*2048*10)

	def __init__(self, *args, **kwargs):
		self.c_album = kwargs.pop('instance', None)
		self.c_user = kwargs.pop('c_user', None)
		super().__init__(*args, **kwargs)

	class Meta:
		model = photo
		fields = ('published','attachments')
	
	def save(self):
		for each in self.cleaned_data['attachments']:
			each.name = rename(each.name)
			new_photo = photo(content=each, albums = self.c_album, user = self.c_user)
			new_photo.filename = each.name
			new_photo.save()


class albumform(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		self.c_user = kwargs.pop('instance', None)
		super().__init__(*args, **kwargs)

	class Meta:
		model = album
		fields = ('title','published','summary')

	def save(self, commit=True):
		album_save=super(albumform, self).save(commit=False)
		album_save.slug = str(self.cleaned_data['title']).replace(" ","-",-1)
		album_save.user = self.c_user
		if commit:
			album_save.save()
		return album_save

class Newuserform(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(Newuserform, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
