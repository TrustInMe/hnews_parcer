from django.test import TestCase, Client

import urllib.request
import bs4 as bs

from .models import Posts

class PostsModelTest(TestCase):
    sause = urllib.request.urlopen('https://news.ycombinator.com/').read()
    soup = bs.BeautifulSoup(sause, 'lxml')

    titles = soup.select('td.title > a')
    
    def setUp(self):
        posts = Posts.objects.bulk_create([
            Posts(title=title.text, url=title['href']) for title in self.titles[0:30]
        ])

        return posts

    def test_employee_creation(self):
        a = self.setUp()
        self.assertTrue(isinstance(a[0], Posts))
        self.assertTrue(isinstance(a[15], Posts))
        self.assertTrue(isinstance(a[26], Posts))
        self.assertTrue(isinstance(a[7], Posts))


class ViewsAccessTest(TestCase):
    client = Client()

    def test_postlist_access(self):
        response = self.client.get('/posts')
        self.assertIs(response.status_code, 200)
