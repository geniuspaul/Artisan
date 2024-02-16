from django.contrib import admin
from .models import User, Skills, Post, Message, Job

admin.site.register(User)
admin.site.register(Skills)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Job)