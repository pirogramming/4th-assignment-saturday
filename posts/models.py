from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=20, unique=False)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()
    scrapped = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    class Meta:
        ordering = ['scrapped']

class Scrapper(models.Model):
    post = models.ForeignKey(Post, related_name='post',on_delete=models.CASCADE, default=None)
    scrapped_by = models.TextField(default=None)
    def get_post(self):
        return self.post
