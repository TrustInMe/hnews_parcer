from django.core.management.base import BaseCommand

import urllib.request
import bs4 as bs

from main.models import Posts

class Command(BaseCommand):
    help = 'Parsing last 30 posts'

    def handle(self, *args, **options):
        sause = urllib.request.urlopen('https://news.ycombinator.com/').read()
        soup = bs.BeautifulSoup(sause, 'lxml')

        titles = soup.select('td.title > a')

        Posts.objects.bulk_create([
            Posts(title=title.text, url=title['href']) for title in titles[0:30]
        ])
        print('done')