from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload, name='upload'),
    path('account/', include('django.contrib.auth.urls')),    
    path('profile/', views.profile, name='profile'),
]
