from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post

class PostList(ListView):
    model = Post
    context_object_name = 'posts' #default context object name is object_list
    template_name = 'index.html'
