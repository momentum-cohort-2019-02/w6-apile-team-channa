from core.models import *


#tendered_submitter = Submitter.objects.get(pk=submitter.pk)

tendered_submitter = 9



submitters_posts = Post.objects.filter(poster_id__exact=tendered_submitter)

SELECT 
"core_post"."id", 
"core_post"."title", 
"core_post"."poster_id", 
"core_post"."description", 
"core_post"."date_added", 
"core_post"."url", 
"core_post"."slug" 
FROM "core_post" WHERE "core_post"."poster_id" = 9 ORDER BY "core_post"."date_added" DESC'

submitters_comments = Comment.objects.filter(commenter_id__exact=tendered_submitter)

SELECT 
"core_comment"."id", 
"core_comment"."commenter_id", 
"core_comment"."post_id", 
"core_comment"."commented_at", 
"core_comment"."text" 
FROM "core_comment" WHERE "core_comment"."commenter_id" = 9 ORDER BY "core_comment"."commented_at" ASC'

other_posts = submitters_comments.select_related('post')

SELECT 
"core_comment"."id",
 "core_comment"."commenter_id",
 "core_comment"."post_id",
 "core_comment"."commented_at", 
 "core_comment"."text", 
 "core_post"."id", 
 "core_post"."title", 
 "core_post"."poster_id", 
 "core_post"."description", 
 "core_post"."date_added", 
 "core_post"."url", 
 "core_post"."slug" 
 FROM "core_comment" INNER JOIN "core_post" ON ("core_comment"."post_id" = "core_post"."id") WHERE "core_comment"."commenter_id" = 9 ORDER BY "core_comment"."commented_at" ASC'

final_post_list = other_posts.union(submitters_posts)
# submit_queryset

(SELECT
 "core_comment"."id", 
 "core_comment"."commenter_id", 
 "core_comment"."post_id", 
 "core_comment"."commented_at", 
 "core_comment"."text", 
 "core_post"."id", 
 "core_post"."title", 
 "core_post"."poster_id", 
 "core_post"."description", 
 "core_post"."date_added", 
 "core_post"."url", 
 "core_post"."slug" 
 FROM "core_comment" INNER JOIN "core_post" ON ("core_comment"."post_id" = "core_post"."id") WHERE "core_comment"."commenter_id" = 9 ORDER BY "core_comment"."commented_at" ASC) UNION (SELECT "core_post"."id", "core_post"."title", "core_post"."poster_id", "core_post"."description", "core_post"."date_added", "core_post"."url", "core_post"."slug" FROM "core_post" WHERE "core_post"."poster_id" = 9 ORDER BY "core_post"."date_added" DESC)'

queryset = final_post_list.all()
# comment_queryset


don't forget to pipenv install


Changes to models.py for Sumbitter models
def get_absolute_url(self):
        return reverse('submitter_detail', args=[str(self.pk)])

Changes to nav link
<a class="nav-link active" href="{% url 'index' %}">Home Advantage</a>

something in urls.py
path('submitter/<int:pk>', views.SubmitterDetailView.as_view(), name='submitter_detail'), 

something in views.py
class SubmitterDetailView(generic.DetailView):
    model = Submitter
    fields = '__all__'