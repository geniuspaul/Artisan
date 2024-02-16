from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from .models import User, Post, Message, Job

    
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Example@tisan.com', 'id': 'put'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '123456789', 'id': 'put'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields.pop('email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('host',)

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('host',)
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('sender', 'reciever')
    body = forms.CharField(widget=forms.TextInput())

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",  "image", "worker")