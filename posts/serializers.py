from rest_framework import serializers
from posts.models import Post, Scrapper, LANGUAGE_CHOICES, STYLE_CHOICES

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'scrapped']

class ScrapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrapper
        fields = ['post']