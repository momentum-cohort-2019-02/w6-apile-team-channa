from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Post, Submitter, Vote, Comment
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse_lazy, reverse


def index(request):
    posts = Post.objects.all()
    submitters = Submitter.objects.all()
    context = {
        'posts': posts,
        'submitters': submitters
    }
    return render(request, 'index.html', context=context)

def sort_by_likes(request):
    """Sorts by number of likes from most to least"""
    posts = Post.objects.annotate(vote_counts=Count('votes')).order_by("-vote_counts","-date_added")

    return render(request, 'index.html', {'posts': posts})

def sort_by_reverse(request):
    """Sorts the date with oldest posts firsts"""
    posts = Post.objects.all().order_by('date_added')
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
    
class CommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a post comment. Requires login. 
    """
    model = Comment
        # define the associated model
    fields = ['text']
        # specify the fields to dislay in the form
        # to specify all fields use <fields = '__all__'> 
        # initial values can also be set for each field using a dictionary
            # 'initital = {'text': 'type your comment here'}

    def get_context_data(self, **kwargs):
        """
        Add associated post to form template so can display its title in HTML.
        Override 'get_context_data()' to pass additional context variables to the template
        """
        context = super(CommentCreate, self).get_context_data(**kwargs)
            # Call the base implementation first to get a context
        context['post'] = get_object_or_404(Post, slug = self.kwargs['slug'])
            # Get the post from id and add it to the context
        return context
        
    def form_valid(self, form):
        """
        Add commenter and associated post to form data before setting it as valid (so it is saved to model)
        Override 'form_valid()' to save additional information when the Comment model is created
        https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-editing/
        """
    
       
        form.instance.commenter = self.request.user.submitter
            # Add logged-in user as commenter of comment
        form.instance.post=get_object_or_404(Post, slug = self.kwargs['slug'])
            # Associate comment with post based on passed id
        return super(CommentCreate, self).form_valid(form)
            # Call super-class form validation behaviour

    def get_success_url(self): 
        """
        After posting comment return to associated post.
        Override 'get_success_url()' to provide somewhere to redirect to, which gets used in the default implementation of 'form_valid()'
        """
        return reverse('post-detail', kwargs={'slug': self.kwargs['slug'],})

   

class PostCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a post. Requires login. 
    """
    model = Post
        # define the associated model
    fields = ['title', 'description', 'url']
        # specify the fields to dislay in the form

    def form_valid(self, form):
        form.instance.poster = self.request.user.submitter
            # Add logged-in user as commenter of comment
        return super(PostCreate, self).form_valid(form)
            # Call super-class form validation behaviour

