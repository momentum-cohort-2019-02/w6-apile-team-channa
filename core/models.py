from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
    # Required to make use of 'User' class
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.
class Submitter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        """String for representing the Submitter objects."""
        return self.user.username
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('submitter_detail', args=[str(self.slug)])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Submitter.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.submitter.save()    


class Post(models.Model):
    """Model representing a post (but not a specific post)."""
    title = models.CharField(max_length=200)

    poster = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the post')
    
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)

    url = models.URLField(max_length=2000, null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True) 

    voted_by = models.ManyToManyField(to=Submitter, related_name='voted_posts', through='Vote')
        # ManyToManyField used b/c users can vote on many posts and posts can have many user votes

    class Meta:
        ordering = ['-date_added',]

    # 'save' and 'set_slug' functions used to automatically create a slug upon saving a post in the admin
    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.poster = request.user
        super().save_model(request, obj, form, change)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.title)
        slug = base_slug
        n = 0
        while Post.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        self.slug = slug[:50]
        
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
        return reverse('post-detail', args=[str(self.slug)])
    
    def get_poster_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('submitter_detail', args=[str(self.poster)])

class Vote(models.Model):
    voter = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#foreign-key-arguments
        # Foreign Key used b/c a user can only upvote a book once, but a user can have many book upvotes
        # 'User' model class argument is declared to connect the relationship between the 'Favorite' and 'User' classes
        # 'on_delete=models.CASCADE' argument deletes the object containing the ForeignKey, thus deletes the instance of the 'Favorite' if 'User' is deleted
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='votes')
        # Foreign Key used b/c a user's upvote can only be on one book, but a book can have many upvotes
    voted_at = models.DateTimeField(auto_now_add=True)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/
        # 'auto_now_add=True' automatically set the field to now when the object is first created
        # useful for creation of timestamps

class Comment(models.Model):
    """
    Model representing a comment on a post
    """
    commenter = models.ForeignKey(Submitter, on_delete=models.CASCADE, null=True)
        # ForeignKey used b/c Comment can only have one author/User, but users can have multiple comments
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Enter comment about post here.")

    class Meta:
        ordering = ["commented_at"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title=75
        if len(self.text) > len_title:
            titlestring = self.text[:len_title] + '...'
        else:
            titlestring = self.text
        return titlestring
       
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.commenter = request.user
        super().save_model(request, obj, form, change)