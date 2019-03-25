from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/add', views.PostCreate.as_view(), name='post_form'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_pk>/vote/', views.post_vote_view, name="post_vote"),
    # intermediary path to display a vote and thus not specific to a template  
    path('sort/by_likes', views.sort_by_likes, name="sort_by_likes"),
    path('sort/oldest', views.sort_by_reverse, name="sort_by_reverse"),
    path('submitters/<int:pk>', views.SubmitterDetailView.as_view(), name="submitter_detail"), 
    path('post/<slug:slug>/comment/', views.CommentCreate.as_view(), name='post_comment'),
]
