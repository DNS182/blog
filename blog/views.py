from django.shortcuts import redirect, render
from . models import Post
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Contact

# Create your views here.
def BlogHome(request):
    posts = Post.objects.all()
    return render(request , 'blog/index.html' , {'posts' : posts})

def search(request):
    query = request.GET.get("query" , "")
    posts = Post.objects.filter(Q(title__icontains = query) | Q(intro__icontains = query))
    return render(request , 'blog/search.html' , {'posts':posts , 'query':query})


def BlogPost(request ,slug):
    post = get_object_or_404(Post , slug = slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.post = post
            msg.user = request.user
            msg.save()
    
    else:
        form = CommentForm()
    return render(request , 'blog/post.html' , {'post':post , 'form':form })


def AboutView(request):
    return render(request , 'blog/about.html')

def ContactView(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        value  = Contact.objects.create(name=name , email=email , subject=subject , message=message)
        value.save()
        redirect('/')

    return render(request , 'blog/contact.html')


def handler404(request, exception):
    response = render(request, "error/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, "error/500.html")
    response.status_code = 500
    return response