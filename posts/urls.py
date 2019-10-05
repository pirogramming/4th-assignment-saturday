from django.urls import path
from posts import views

urlpatterns = [
    path('',views.post_list),
    path('login/', views.login),
    path('posts/', views.post_list),
    path('posts/<int:pk>/', views.post_detail),
    path('posts/create', views.post_create),
    path('posts/update', views.post_update),
    path('posts/delete', views.post_delete),
    path('posts/scrap', views.post_scrap),
    path('my/', views.my),
    path('logout/', views.logout),
    path('posts/unscrap', views.unscrap)
]