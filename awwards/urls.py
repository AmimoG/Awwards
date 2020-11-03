from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name='profile'),
    path('account/', include('django.contrib.auth.urls')),
    path('post/', views.post, name='post')
]
