from django.shortcuts import render

# Create your views here.
from .models import *

from .forms import *

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

 

def post_list(request):

    posts = Post.objects.all().order_by('-date_created')

    return render(request, 'reddit/post_list.html',  {'posts': posts})

@login_required

def post_new(request):

    if request.method == "POST":

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.submitter = request.user

            post.save()

            for subreddit_id in request.POST.getlist('subreddits'):

                SubRedditPost.objects.create(subreddit_id=subreddit_id, post=post)

            return redirect('post_detail', pk=post.pk)

    else:

        form = PostForm()

    return render(request, 'reddit/post_edit.html', {'form': form, 'is_create': True})

@login_required

def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":

        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            post = form.save(commit=False)

            post.save()

            return redirect('post_detail', pk=post.pk)

    else:

        form = PostForm(instance=post, initial={'subreddits' : post.subreddits.all()})

    return render(request, 'reddit/post_edit.html', {'form': form, 'is_create': False})

def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    return render(request, 'reddit/post_detail.html', {'post': post})

def sub_detail(request, pk):

    sub = get_object_or_404(SubReddit, pk=pk)

    return render(request, 'reddit/sub_detail.html', {'sub': sub})

@login_required

def add_comment(request, pk, parent_pk=None):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post

            comment.author = request.user

            comment.parent_id = parent_pk

            comment.save()

        return redirect('post_detail', pk=post.pk)

    else:

        form = CommentForm()

    return render(request, 'reddit/add_comment.html', {'form': form})


