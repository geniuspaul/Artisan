from django.urls import path
from .views import index, signup, logoutview, postdetail, jobdetail, account, profile, createpost, find, deletepost, deletejob, order, chat, editprofile
from django.contrib.auth.views import LoginView
from .forms import LoginForm
app_name = "core"
urlpatterns = [
    path('', index, name="index"),
    path('signup/', signup, name="sign-up"),
    path('login/', LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm, redirect_authenticated_user = True), name='log-in'),
    path('find/', find, name='find'),
    path('chat/order/<str:pk>/', chat, name='chat'),
    path('order/', order, name='order'),
    path('account/', account, name='account'),
    path('delete/<str:pk>', deletepost, name='delete-post'),
    path('deletes/<str:pk>', deletejob, name='delete-job'),
    path('create-post/', createpost, name='create-post'),
    path('account/profile/<str:pk>/', profile, name='profile'),
    path('account/profile/edit/<str:pk>/', editprofile, name='edit-profile'),
    path('logout/', logoutview, name='log-out'),
    path('detail/<str:pk>/', postdetail, name='detail'),
    path('details/<str:pk>/', jobdetail, name='job-detail'),
]
