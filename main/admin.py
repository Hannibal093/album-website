from django.contrib import admin
from .models import category, album, photo
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class Photography_site(admin.ModelAdmin):
	fieldsets = [
		("Title/date", {"fields": ["album.title", "album.published"]}),
		("URL", {"fields":["album.slug"]}),
		("Album", {"fields":["albums"]}),
	]

	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}

admin.site.register(photo)
admin.site.register(album)
admin.site.register(category)