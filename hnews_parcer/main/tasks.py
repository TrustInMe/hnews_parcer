from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab

from .models import Posts

import urllib.request
import bs4 as bs


@periodic_task(run_every=crontab(minute='*/5'))
def parse():
    Posts.objects.all().delete()

    print('deleting complete')

    sause = urllib.request.urlopen('https://news.ycombinator.com/').read()
    soup = bs.BeautifulSoup(sause, 'lxml')

    titles = soup.select('td.title > a')

    Posts.objects.bulk_create([
        Posts(title=title.text, url=title['href']) for title in titles[0:30]
    ])
    print('done')