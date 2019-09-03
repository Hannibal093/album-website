from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import category, photo, album
from django.http import HttpResponse
from .forms import photoform, Newuserform, albumform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from .apitest import *

# Create your views here.

bucket_prefix = 'hannibal-album-'
localfolder_prefix = 'C:/Users/syringalin/Desktop/django_project/mysite/media/images/'

def index(request):
	if request.user:
		matching_album=album.objects.filter(user__username=request.user.username).order_by('published')
		fst_photo = []
		for a in matching_album:
			if photo.objects.filter(albums__slug=a.slug):
				fst_photo.append(photo.objects.filter(albums__slug=a.slug).earliest("published").content.url) 
			else:
				fst_photo.append('/media/images/album_cover_default.jpg')
		collect = zip(matching_album,fst_photo)
		return render(request,
					template_name="main/albums.html",
					context={"collect":collect})
	else:
		return render(request,
					  template_name="main/albums.html")

def register(request):
	if request.method=="POST":
		form = Newuserform(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New Account Created: {username}")
			new_bucket('hannibal-album-' + username)
			login(request, user)
			messages.info(request, f"You are now logged in as {username}")
			return redirect("main:index")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")
	form = Newuserform
	return render(request,"main/register.html",{"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully! Redirect to Homepage.")
	return redirect("main:index")

def login_request(request):
	if request.method=="POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				current_user=request.user.username
				bucket_check(current_user)
				request.session['cur_user']=current_user
				messages.info(request,f'You are now logged in as {username}')
				return redirect("main:index")
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request,"main/login.html",{"form":form})
	
def upload_photo(request, a_slug):
	pk = get_object_or_404(album, slug=a_slug).pk
	current_user = request.user
	current_album = get_object_or_404(album.objects, pk=pk)
	if request.method == 'POST':
		form = photoform(request.POST, request.FILES, instance=current_album, c_user = current_user)
		if form.is_valid():
			form.save()
			upload_blob(bucket_prefix + current_user.username, current_album.title, localfolder_prefix + current_user.username + '/')
			return redirect('main:single_slug',current_album.slug)
	else:
		form = photoform(instance=current_album, c_user = current_user)
	return render(request, 'main/upload_photo.html', {'form':form,'c_album':current_album})

def add_new(request):
	current_user = request.user
	print(current_user.username)
	if request.method=='POST':
		form = albumform(request.POST, instance=current_user)
		if form.is_valid():
			form.save()
			return redirect("main:index")
	else:
		form = albumform(instance=current_user)
	return render(request, "main/add_new.html", {"form":form})

def single_slug(request, single_slug):
	albums = [ab.slug for ab in album.objects.all()]
	if single_slug in albums:
		matching_photos = photo.objects.filter(albums__slug=single_slug).order_by("published")
		filenames = [str(mp.content.url).split('/')[-1] for mp in matching_photos]
		album_idx = album.objects.only('id').get(slug=single_slug).id
		request.session['album_idx'] = album_idx
		return render(request,
					  'main/photos.html',
					  context={"photos":matching_photos,"c_album":album_idx, "a_slug":single_slug, "c_user":request.user.username, "fn":filenames})
	return HttpResponse(f"{single_slug} is not corresond to anything.")

def delete_obj(request, pk, c_album, level):
	if request.method=="POST":
		current_album = get_object_or_404(album.objects, pk=c_album)
		if level==1:
			current_album.delete()
			return redirect("main:index")
		elif level==2:
			photos = photo.objects.get(pk=pk)
			url = str(photos.content.url)
			filename = url.split('/')[-1]
			d_filelist = []
			d_filelist.append(filename)
		
			delete_blob(request.user.username, current_album.title, d_filelist)
			photos.delete()
			return redirect('main:single_slug', single_slug = current_album.slug)

def bucket_check(current_user):
	client = storage.Client()
	if not client.get_bucket(bucket_prefix + current_user):
		new_bucket(bucket_prefix + current_user)
