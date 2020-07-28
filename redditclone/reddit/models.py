from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
import uuid

class BaseModel(models.Model):

    eid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta: abstract = True

    # Helper method, so that we don't have to do the existence check every time.

    @classmethod

    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)

        except cls.DoesNotExist:
            return None

class SubReddit(BaseModel):
    name = models.CharField(max_length=200)
    posts = models.ManyToManyField('Post', related_name='subreddits', blank=True, through='SubRedditPost')
    cover_image_url = models.URLField('Cover Image URL', max_length=200, blank=True, null=True )
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subreddits_moderated')

    def __str__(self):
        return self.name

 

class SubRedditPost(BaseModel):
    subreddit = models.ForeignKey('SubReddit', related_name='posts_set', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='subreddits_set', on_delete=models.CASCADE)
 
    class Meta: unique_together = ['subreddit', 'post']

 

class Votable(BaseModel):
    upvote_count = models.PositiveIntegerField(default=0)
    downvote_count = models.PositiveIntegerField(default=0)
    class Meta: abstract = True

 

class Post(Votable):
    title = models.CharField(max_length=200)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts_submitted', on_delete=models.CASCADE)
    url = models.URLField('URL', max_length=200, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    comment_count = models.PositiveIntegerField(default=0)

    def children(self):

        return self.comments.filter(parent=None)

    def __str__(self):

        return str(self.eid) + ": " + self.title

 

class Comment(Votable):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments_authored', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

 

    def __str__(self):

        return str(self.eid) + ": " + self.text

 

 

class UserVote(BaseModel):

    UP_VOTE = 'U'

    DOWN_VOTE = 'D'

    VOTE_TYPE = (

        (UP_VOTE, 'Up Vote'),

        (DOWN_VOTE, 'Down Vote')

    )

 

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes', on_delete=models.CASCADE)

    #Generic Foreign Key config

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.UUIDField()

    content_object = GenericForeignKey('content_type', 'object_id')

 

    vote_type = models.CharField(max_length=1, choices=VOTE_TYPE)

 

    class Meta: unique_together = ['voter', 'object_id', 'content_type']