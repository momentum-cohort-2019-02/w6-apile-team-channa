from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
    # Required to make use of 'User' class

# Create your models here.
class Submitter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Post(models.Model):
    """Model representing a post (but not a specific post)."""
    title = models.CharField(max_length=200)

    poster = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the post')
    
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)

    url = models.URLField(max_length=2000, null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True) 

    commented_by = models.ManyToManyField(to=Submitter, related_name='commented_posts')
        # ManyToManyField used b/c users can comment on many posts and posts can have many user comments
        # 'through' option allows an intermediate table to be specified
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-types

    voted_by = models.ManyToManyField(to=Submitter, related_name='voted_posts', through='Vote')
        # ManyToManyField used b/c users can vote on many posts and posts can have many user votes

    class Meta:
        ordering = ['-date_added',]
        
    def display_voted_by(self):
        """Create a string for the upvoted_by field. This is required to display voted_by in Admin."""
        return ', '.join(voted_by.username for voted_by in self.voted_by.all()[:3])
            # str.join(iterable) --> https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join
            # 1st three '[:3]' upvoted_by items in the 'self.upvoted_by.all()' for a 'Post' object will be joined separated by a comma ', '

    display_voted_by.short_description = 'voted_by_user'
        # '.short_description' is a built-in Django attribute to provide human-readable descriptions for callback functions
        # https://docs.djangoproject.com/en/2.1/ref/contrib/admin/actions/

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('index')

class Vote(models.Model):
    voter = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#foreign-key-arguments
        # Foreign Key used b/c a user can only upvote a book once, but a user can have many book upvotes
        # 'User' model class argument is declared to connect the relationship between the 'Favorite' and 'User' classes
        # 'on_delete=models.CASCADE' argument deletes the object containing the ForeignKey, thus deletes the instance of the 'Favorite' if 'User' is deleted
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
        # Foreign Key used b/c a user's upvote can only be on one book, but a book can have many upvotes
    voted_at = models.DateTimeField(auto_now_add=True)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/
        # 'auto_now_add=True' automatically set the field to now when the object is first created
        # useful for creation of timestamps

class Comment(models.Model):
    commenter = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
       