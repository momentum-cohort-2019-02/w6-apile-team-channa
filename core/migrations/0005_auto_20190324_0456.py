# Generated by Django 2.1.7 on 2019-03-24 08:56
# started by running '$ ./manage.py makemigrations --empty core'

from django.db import migrations
from django.conf import settings
import os.path
import csv
from django.core.files import File
from django.utils.text import slugify
from django.contrib.auth.models import User


def load_post_data(apps, schema_editor):
    """
    Read a CSV file full of posts and insert them into the database
    """
    Post = apps.get_model('core', 'Post')
        # https://docs.djangoproject.com/en/2.1/ref/applications/#application-registry
        # 'apps.get_model(app_label, model_name, require_ready=True)' returns the 'Post' model in the 'core' app
    Submitter = apps.get_model('core', 'Submitter')
    User = apps.get_model('auth', 'User')

    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
        # data to be read is stored in the 'initial_data' directory
    datafile = os.path.join(datapath, 'posts.csv')
        # data file to be read is named 'books.csv'
    Post.objects.all().delete()
        # delete all existing 'Post' objects in the database
    Submitter.objects.all().delete()
        # delete all existing 'Submitter' objects in the database

    with open(datafile) as file: 
        reader = csv.DictReader(file)
            # https://docs.python.org/3.7/library/csv.html?highlight=csv%20dictreader#csv.DictReader
            # 'csv.DictReader' creates an object that operates like a regular reader but maps the information in each row to an 'OrderedDict' whose keys are given by the optional fieldnames parameter
            # if fieldnames is omitted (as we do here), the values in the first row of the file will be used as the fieldnames
        for row in reader:
            post_title = row['title']
            if Post.objects.filter(title=post_title).count():
                continue
                    # if a post with that title already exists, then skip the rest of the statements in the loop and 'continue' on to the next iteration of the loop
                    # prevents duplicate posts
            if User.objects.filter(username=row['poster']).count():
                user = User.objects.filter(username=row['poster'])[0]
                if Submitter.objects.filter(user=user).count():
                    submitter = Submitter.objects.filter(user=user)[0]
                else:
                    submitter, _ = Submitter.objects.get_or_create(user=user)
            else:
                user, _ = User.objects.get_or_create(username=row['poster'])
                user.save()
                submitter, _ = Submitter.objects.get_or_create(user=user)
                # submitter = Submitter(
                #     user=user,
                # )

            submitter.save()

            post = Post(
                title=row['title'],
                description=row['description'],
                url=row['url'],
                poster=submitter,
            )
            post.save()

            if row['slug'] == '':
                base_slug = slugify(row['title'])
                slug = base_slug
                n = 0
                while Post.objects.filter(slug=slug).count():
                    n += 1
                    slug = base_slug + "-" + str(n)
                post.slug = slug[:50]
            post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190322_1402'),
    ]

    operations = [
        migrations.RunPython(load_post_data)
    ]
