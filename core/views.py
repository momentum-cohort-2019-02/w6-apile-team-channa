from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Submitter, Vote, Comment
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User

# class PostList(generic.ListView):
#     model = Post
#     context_object_name = 'posts' #default context object name is object_list
#     template_name = 'index.html'

def index(request):
    posts = Post.objects.all()
    submitters = Submitter.objects.all()
    context = {
        'posts': posts,
        'submitters': submitters
    }
    return render(request, 'index.html', context=context)

class PostDetailView(generic.DetailView):
    """View class for author page of site."""
    model = Post

@require_http_methods(['POST'])
    # view decorator to require that only Post requests are accepted
    # https://docs.djangoproject.com/en/dev/topics/http/decorators/#
@login_required
    # view decorator to require that the user is logged in
    # https://docs.djangoproject.com/en/dev/topics/auth/default/
def post_vote_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
        # 'get_object_or_404()' function takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the 'get()' function of the model's manager
        # It raises 'Http404' if the object does not exist
    next = request.POST.get('next', '/')
        # https://docs.djangoproject.com/en/2.1/ref/request-response/
        # 'request' is just an object of the 'HttpRequest' class
        # '.POST' is a dictionary-like object containing all given HTTP POST paramenters, providing that the request contains form data
        # '.get(key, default=None)' returns the 'next' key, but will return '/' (home page) if 'next' key does not exist

    vote, created = request.user.submitter.vote_set.get_or_create(post=post)
        # '.get_or_created()' function returns a tuple of (object, created), where 'object' is the retrieved or created object and 'created' is a boolean specifying whether a new object was created
        # here, we're getting a favorite object corresponding to the book object...if there is one, then assign it to the variable 'favorite'.
        # if there isn't one, then create one and assign it to the variable 'favorite'
        # since it returns a tuple, we need to add the comma after 'favorite' variable declaration to declare another variable 'created' to capture True or False

    if created: # if the favorite object was newly created:
        messages.success(request, f"You have voted {post.title}")
            # https://docs.djangoproject.com/en/dev/ref/contrib/messages/
    else: # if the favorite object already existed
        messages.info(request, f"You have unvoted {post.title}")
        vote.delete()
            # deletes the favorite object

    return HttpResponseRedirect(next)
        # redirects back to the current page