from django.contrib import admin
from django.urls import path, include
from main.views import PostsView, IndexView, ButtonParceView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('parce', ButtonParceView.as_view(), name='button'),
    path('posts', PostsView.as_view(), name='posts'),
    path('admin/', admin.site.urls),
]
