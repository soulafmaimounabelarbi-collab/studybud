from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Feedback,Content

#admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Feedback)
admin.site.register(Content)