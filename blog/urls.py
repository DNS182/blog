from django.urls import path , include
from . import views

urlpatterns = [
    path('' , views.BlogHome , name='bloghome'),
    path('search' , views.search , name= 'search'),
    path('about/' , views.AboutView , name='about'),
    path('contact/' , views.ContactView , name='contact'),
    path('<slug:slug>/' , views.BlogPost , name='blogpost'),
        
]

handler404 = 'blog.views.handler404'
handler500 = 'blog.views.handler500'