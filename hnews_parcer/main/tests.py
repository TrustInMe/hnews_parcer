from django.test import TestCase, Client
from rest_framework.test import APITestCase

import urllib.request
import bs4 as bs
import urllib.request
import json

from .models import Posts
from .views import PostsView

class PostsModelTest(TestCase):
    """ Тестируем правильный парсинг и создание модели """

    def setUp(self):
        sause = urllib.request.urlopen('https://news.ycombinator.com/').read()
        soup = bs.BeautifulSoup(sause, 'lxml')

        titles = soup.select('td.title > a')

        posts = Posts.objects.bulk_create([
            Posts(title=title.text, url=title['href']) for title in titles[0:30]
        ])

        return posts

    def test_post_creation(self):
        a = self.setUp()
        self.assertTrue(isinstance(a[0], Posts))
        self.assertTrue(isinstance(a[15], Posts))
        self.assertTrue(isinstance(a[26], Posts))
        self.assertTrue(isinstance(a[7], Posts))


class ViewsAccessTest(TestCase):
    """ Тестируем доступ к страницам """

    client = Client()

    def test_index_access(self):
        response = self.client.get('asdas')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('')
        self.assertIs(response.status_code, 200)


    def test_postlist_access(self):
        urls = [
            '/posts',
            '/posts?offset=2', 
            '/posts?limit=3', 
            '/posts?order=-id', 
            '/posts?order=-id&offset=2&limit=3'
            ]

        for url in urls: 
            response = self.client.get('/posts')
            self.assertIs(response.status_code, 200)
    
    def test_parse_buton(self):
        response = self.client.get('/parse')
        self.assertEqual(response.status_code, 302)


class LimitTests(APITestCase):
    """ Тестируем парамерт limit """
    
    def test_default_limit(self):
        PostsModelTest.setUp(self)
        response = self.client.get('/posts', format='json')
        self.assertEqual(len(response.data), 5)

    def test_custom_limit(self):
        PostsModelTest.setUp(self)
        response = self.client.get('/posts?limit=1', format='json')
        self.assertEqual(len(response.data), 1)

    def test_max_limit(self):
        PostsModelTest.setUp(self)
        response = self.client.get('/posts?limit=26', format='json')
        self.assertEqual(len(response.data), 25)

class OrderOffsetTests(APITestCase):
    """ Тестируем парамерты offset и order """

    def test_order(self):
        PostsModelTest.setUp(self)
        response = self.client.get('/posts?order=-id', format='json')
        self.assertEqual(response.data[0]['id'], 30)

        response = self.client.get('/posts?order=id&offset=1', format='json')
        self.assertEqual(response.data[0]['id'], 2)

        response = self.client.get('/posts?order=-id&offset=5', format='json')
        self.assertEqual(response.data[2]['id'], 23)

        response = self.client.get('/posts?order=-id&offset=5&limit=1', format='json')
        self.assertEqual(response.data[0]['id'], 25)
