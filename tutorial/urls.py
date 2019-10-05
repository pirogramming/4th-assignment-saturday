from django.urls import path, include

urlpatterns = [
    # path('', include('snippets.urls')),
    path('', include('posts.urls')),
]
