from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import url,include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login, authenticate
from django.conf.urls.static import static
from .models import Profile, Image
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import AddPostForm


@login_required(login_url='/accounts/login/')
def index(request):
    all_images = Image.objects.all()
    all_users = Profile.objects.all()
    current_user = request.user
    next = request.GET.get('next')
    if next: return redirect(next)
    return render(request, 'display/home.html',  {"all_images": all_images, "current_user":current_user, "all_users":all_users})


def image_location(request, location):
    images = Image.filter_by_location(location)
    print(images)
    return render(request, 'insta/location.html', {'location_images': images})


def search_results(request):
    if 'imagesearch' in request.GET and request.GET["imagesearch"]:
        category = request.GET.get("imagesearch")
        searched_images = Image.search_by_category(category)
        message = f"{category}"
        print(searched_images)
        return render(request, 'display/eplore.html', {"message": message, "images": searched_images})
    else:
        message = "You haven't searched for any image category"
        return render(request, 'display/explore.html', {"message": message})


@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'display/userprofile.html')


def post(request):
    return render(request, 'display/post.html')


@login_required(login_url='/accounts/login/')
def upload(request):
    current_user = request.user
    p = Profile.objects.filter(id=current_user.id).first()
    imageuploader_profile = Image.objects.filter(imageuploader_profile=p).all()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.imageuploader_profile= p
            post.save()
            return redirect('index')
    else:
        form =PostForm
    return render(request, 'display/home.html', {"form": form})

def signup(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'registration/registration_form.html', {'form': form})


# adding post and or images

@login_required(login_url='/accounts/login/')
def post(request):
    current_user = request.user

    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user= current_user
            post.save()
        return redirect('/')
    else:
        form = AddPostForm()
    return render(request, 'new_post.html', {'current_user':current_user, 'form':form}) 
