from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SignupForm, PostForm, MessageForm, EditForm, JobForm
from django.db.models import Q
from django.contrib.auth import logout
from .models import Post, User, Skills, Message, Job
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'core/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('core:log-in') 
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'core/signup.html', context)

@login_required()
def logoutview(request):
    logout(request)
    return redirect("core:log-in")

@login_required()
def postdetail(request, pk):
    post = get_object_or_404(Post, id=pk)
    ins = 'post'
    related = Post.objects.filter(skill=post.skill)[:5]
    context = {'post':post, 'related_items':related, 'ins':ins}
    return render(request, "core/detail.html", context)

@login_required()
def jobdetail(request, pk):
    post = get_object_or_404(Job, id=pk)
    ins = ''
    related = Job.objects.filter(skill=post.skill)[:5]
    context = {'post':post, 'related_items':related, 'ins':ins}
    return render(request, "core/detail.html", context)

@login_required()
def createpost(request):
    form = ''
    posts = ''
    user = get_object_or_404(User, id=request.user.id)
    if user.worker:
        posts = Post.objects.filter(host__id=user.id)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.host = request.user
                instance.save()
                return redirect('core:create-post') 
        else:
            form = PostForm()
    else:
        posts = Job.objects.filter(host__id=user.id)
        if request.method == 'POST':
            form = JobForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.host = request.user
                instance.save()
                return redirect('core:create-post') 
        else:
            form = JobForm()
    context = {'form': form, 'posts':posts[:5], 'user':user}
    return render(request, "core/create-post.html", context)

@login_required()
def account(request):
    return render(request, "core/account.html")

@login_required()
def profile(request, pk):
    user = get_object_or_404(User, id=pk)
    if user.worker:
        posts = Post.objects.filter(host=user)
    else:
        posts = Job.objects.filter(host=user)
    paginator = Paginator(posts, per_page=10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    context = { "current_page":current_page, 'user':user, "posts":posts}
    return render(request, "core/profile.html", context)

@login_required()
def find(request):
    q = request.GET.get('q', '').strip()
    posts = ''
    if request.user.worker:
        if q:
            posts = Job.objects.filter(Q(skill__name__icontains=q)|Q(title__icontains=q)|Q(host__username=q))
        else:
            posts = Job.objects.all()
    else:
        if q:
            posts = Post.objects.filter(Q(skill__name__icontains=q)|Q(title__icontains=q)|Q(host__username=q))
        else:
            posts = Post.objects.all()

    skills = Skills.objects.all()
    per_page = 0
    paginator = Paginator(posts, per_page=6)
    page = request.GET.get('page')
    
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {'current_page': current_page, 'skills': skills, 'search_query': q, "posts":posts[:6]}
    return render(request, "core/find.html", context)

@login_required()
def deletepost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect("core:find")
    context = {'post':post,}        
    return render(request, "core/delete.html", context)

@login_required()
def deletejob(request, pk):
    post = get_object_or_404(Job, id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect("core:find")
    context = {'post':post}        
    return render(request, "core/delete.html", context)

@login_required()
def order(request):
    user_order = Message.objects.filter(
        Q(sender__id=request.user.id) | Q(reciever__id=request.user.id)
    ).distinct()
    user_order = set(user_order)
    context = {"users_orders": user_order}
    return render(request, "core/order.html", context)


@login_required()
def chat(request, pk):
    friend = get_object_or_404(User, id=pk)
    sms = Message.objects.filter(
        Q(sender__id=request.user.id, reciever__id=pk)|
        Q(reciever__id=request.user.id, sender__id=pk)
    ).reverse()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.reciever = friend
            instance.save()
            return redirect("core:chat",pk)
    else:
        form = MessageForm()
    context = {"smss":sms, 'form':form, 'friend':friend}
    return render(request, "core/order-field.html", context)

@login_required()
def editprofile(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("core:profile", pk)
    else:
        form = EditForm(instance=user)
    context = {"user":user, "form":form}
    return render(request, "core/edit-profile.html", context)
    
    
