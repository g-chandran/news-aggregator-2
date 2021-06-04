from bs4 import BeautifulSoup
from .models import Article, Subscription
import feedparser as fp
import pytz
from dateutil.parser import parse as p
from celery import shared_task
import requests


@shared_task(name="start_aggregating")
def aggregator():
    if not isNetworkAvailable():
        print("No internet available")
        return
    updateList = []
    try:
        subscriptions = Subscription.objects.all()
    except Exception as e:
        print(e)
        print("Exception occured at fetching data from Database. Check the Database connection")
        return
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
                    author = ' ' if not feed.has_key("author") else feed.author
                    summary = getSummary(feed.summary)
                    media = getMedia(feed)
                    article_as_list = getArticle(link)
                    article = " " if article_as_list is None else "\n".join(
                        article_as_list)
                    converted_time = p(pubTime)
                    try:
                        a = Article.objects.create(subscription_name=subscription, published=converted_time, title=title,
                                                   author=author, summary=summary, media=media, article_id=iD, article_link=link, article=article)
                        a.save()
                    except Exception as e:
                        print(e)
                        print("Exception occurred at Saving the data")
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


def getArticle(url):
    try:
        page = requests.get(url)
    except Exception as e:
        print(e)
        print("Exception occured at requesting the page from RSS at: " + url)
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    p_tags = soup.find_all('p')
    article = list(map(lambda x: str(x.text), p_tags))
    return article if len(article) != 0 else None


def isNetworkAvailable(url="http://www.google.com/", timeout=3):
    try:
        requests.head(url, timeout)
        return True
    except requests.ConnectionError as ex:
        print(ex)
        return False
