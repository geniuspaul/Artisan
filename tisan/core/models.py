from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class Skills(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'skills'
    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    image = models.ImageField(default='images/avarter.png', upload_to='images/')
    stars = models.IntegerField(default=0)
    worker = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='skill')
    title = models.CharField(max_length=50)
    cost = models.IntegerField(default=10000)
    negotiable = models.BooleanField(default=True)
    image = models.ImageField(upload_to="images/")
    description = models.TextField(default='', max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['skill']
        
    def __str__(self) -> str:
        return f"Title:  {self.title}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    body = models.TextField(default='')
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) :
        return f"{self.sender} to {self.reciever}  {self.body[:15]}"
class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, related_name='needed_skill')
    title = models.CharField(max_length=50)
    cost = models.IntegerField(default=10000)
    negotiable = models.BooleanField(default=True)
    image = models.ImageField(upload_to="images/")
    description = models.TextField(default='', max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['skill']
        
    def __str__(self) -> str:
        return f"Title:  {self.title}"
    
    