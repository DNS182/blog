from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login' , auth_views.LoginView.as_view(template_name='account/login.html') , name='login'),
    path('logout' , auth_views.LogoutView.as_view(template_name='account/logout.html')   , name='logout'),
    path('register' , views.register , name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'), 
    path('profile' , views.profile  , name='profile'),
    path('profile-edit' , views.profile_edit  , name='profile-edit'),
]
