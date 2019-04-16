from django.views import View
from django.shortcuts import render, redirect

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination)

from .models import Posts
from .serializers import PostSerializer

import urllib.request
import bs4 as bs


class IndexView(View):
    def get(self, request):
        posts = Posts.objects.all()
        return render(self.request, 'index_temp.html', {
            'posts': posts
        })

class ButtonParceView(View):
    def get(self, request):
        posts = Posts.objects.all().delete()
        
        sause = urllib.request.urlopen('https://news.ycombinator.com/').read()
        soup = bs.BeautifulSoup(sause, 'lxml')

        titles = soup.select('td.title > a')

        Posts.objects.bulk_create([
            Posts(title=title.text, url=title['href']) for title in titles[0:30]
        ])
        return redirect('index')


class PostsView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = '__all__'

    paginator = LimitOffsetPagination()
    paginator.default_limit = 5
    paginator.max_limit = 25

    def get_paginated_response(self, data):
       return Response(data)


