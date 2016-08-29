from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect

#### added by ashish
from django.http import *
import json
from django.views.generic.base import View
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/post_detail.html',{'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

########## for API practice #######
class post_list_api(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(post_list_api, self).dispatch(*args, **kwargs)
    def post(self,request):
        post_data = json.loads(request.body.decode('utf-8'))
        auth_name = post_data.get('author_name') or ''
        postlist = []
        if auth_name == "all":
            posts = Post.objects.all()
            for post in posts:
                titleName = post.title
                postlist.append(titleName)
            return HttpResponse(json.dumps(postlist))
        else:
            posts = Post.objects.filter(author=auth_name)
            for post in posts:
                titleName = post.title
                postlist.append(titleName)
            return HttpResponse(json.dumps(postlist))

    
