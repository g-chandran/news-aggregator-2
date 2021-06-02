from bs4 import BeautifulSoup
from .models import Article, Subscription
import feedparser as fp
import pytz
from dateutil.parser import parse as p
from celery import shared_task


@shared_task
def aggregator():
    updateList = []
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        feeds = fp.parse(subscription.feed_url)
        if p(feeds.entries[0].published) != subscription.last_updated:
            subscription.last_updated = p(feeds.entries[0].published)
            subscription.save()
            print('Updating: ' + str(subscription.name))
            updateList.append(subscription.name)
            for feed in feeds.entries:
                if Article.objects.filter(article_id=feed.id).count() == 0:
                    pubTime = feed.published
                    title = feed.title
                    link = feed.link
                    iD = feed.id
                    summary = getSummary(feed.summary)
                    author = ' ' if not feed.has_key("author") else feed.author
                    media = getMedia(feed)
                    converted_time = p(pubTime).astimezone(
                        pytz.timezone('Asia/Kolkata'))
                    a = Article.objects.create(subscription_name=subscription, published=converted_time, title=title,
                                               author=author, summary=summary, media=media, article_id=iD, article_link=link)
                    a.save()
            print(f"{subscription.name} done")
    print(updateList)


def getSummary(text):
    if len(text) >= 400:
        return text[0:396] + "..."
    return text


def getMedia(entry):
    if entry.has_key('media_content'):
        media = entry.media_content[0]['url']
    elif entry.has_key('links'):
        media = entry.links[1]['href']
    else:
        html = BeautifulSoup(entry.summary, "html.parser")
        media = html.find('img')['src']
    return media
