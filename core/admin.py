from django.contrib import admin
from core.models import Post, Vote, Submitter, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ('title', 'poster', 'date_added')
   list_filter = ('date_added', 'poster')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
   list_display = ('voter', 'post', 'voted_at')

@admin.register(Submitter)
class SubmitterAdmin(admin.ModelAdmin):
   list_display = ('user', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_display = ('commenter', 'post', 'commented_at', 'text')