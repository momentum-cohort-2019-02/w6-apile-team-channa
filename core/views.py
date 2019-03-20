from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post

# class PostList(generic.ListView):
#     model = Post
#     context_object_name = 'posts' #default context object name is object_list
#     template_name = 'index.html'

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'posts':posts
    })

# @login_required
# def make_post(request):
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = Post(**form.cleaned_data)
#             post.author = request.user
#             post.slug = slugify(post.title)
#             post.save()
#             messages.add_message(request,
#             messages.INFO,
#             'Your post was published.')
#         return redirect('home')
#     return render(request, 'posts/post_form.html', {
#         'form': form
#     })
