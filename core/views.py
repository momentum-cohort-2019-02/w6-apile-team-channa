from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Submitter, Vote, Comment
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count

def index(request):
    posts = Post.objects.select_related('poster')
    context = {
        'posts': posts,
        
    }
    return render(request, 'index.html', context=context)

def sort_by_likes(request):
    """Sorts by number of likes from most to least"""
    posts = Post.objects.annotate(vote_counts=Count('votes')).order_by("-vote_counts","-date_added")

    return render(request, 'index.html', {'posts': posts})

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

class SubmitterDetailView(generic.DetailView):
    model = Submitter
    fields = '__all__'

def SubmitsView(request, **kwargs):
    #tendered_submitter = get_object_or_404(Submitter, pk=submitter_pk)
    #tendered_submitter = Submitter.objects.get(pk=submitter.pk)
    tendered_submitter = kwargs.get(submitter.id)
    submitters_posts = Post.objects.filter(poster_id__exact=tendered_submitter)
    submitters_comments = Comment.objects.filter(commenter_id__exact=tendered_submitter)
    other_posts = submitters_comments.select_related('post')
    final_post_list = other_posts.values_list("title", "poster", "description", "date_added", "url", "slug", "voted_by").union(submitters_posts.values_list("title", "poster", "description", "date_added", "url", "slug", "voted_by"))
    submit_queryset = final_post_list.all()
    context = {
        'posts': post,
        'comment': comment
        }
    return render(request, 'submit_list.html', context=context)

def CommentListView(requst, **kwargs):
    #tendered_submitter = get_object_or_404(Submitter, pk=submitter_pk)
    #tendered_submitter = Submitter.objects.get(pk=submitter.pk)
    tendered_submitter = kwargs.get(submitter.id)
    submitters_posts = Post.objects.filter(poster_id__exact=tendered_submitter)
    submitters_comments = Comment.objects.filter(commenter_id__exact=tendered_submitter)
    comment_queryset = submitters_comments.all()
    context = {
        'post': post,
        'comment': comment
        }
    return render(request, 'comment_list.html', context=context)
