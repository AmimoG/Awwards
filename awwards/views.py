from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Profile
from .forms import *

# view functions created from here

def index(request):
    return render(request, 'award/index.html')


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return render(request, 'award/profile.html')


def post(request):
    current_user = request.user
    try:
        profile = Profile.objects.get(user = current_user)
    except:
        return redirect('edit_profile',username = current_user.username)

    try:
        posts = Post.objects.filter(neighborhood = profile.neighborhood)
    except:
        posts = None

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=current_user
            post.neighborhood = profile.neighborhood
            post.save()
        return redirect('index')
    else:
        form = PostForm()
   
    return render(request, 'award/post.html', {'posts': posts, 'form': form})
