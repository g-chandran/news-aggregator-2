from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404, render
from .models import Subscription, Profile, Article

from dateutil.parser import parse as p
from bs4 import BeautifulSoup
import feedparser as fp
import pytz


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


def aggregator(request):
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
    # return render(request, 'aggregator.html', {'updateList': updateList})


class HomeListView(ListView):
    model = Article
    template_name = "home.html"
    context_object_name = "articles"
    paginate_by = 20

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            subscription_object = Profile.objects.filter(name=current_user)
            subscriptions = [
                object.subscription for object in subscription_object]
            result = Article.objects.filter(
                subscription_name__in=subscriptions).order_by('-published')
            return result
        else:
            return Article.objects.all().order_by('-published')


class SubscriptionListView(ListView):
    model = Article
    template_name = "subscription.html"
    context_object_name = "articles"
    paginate_by = 20

    def get_queryset(self):
        subscriptions = get_object_or_404(
            Subscription, name=self.kwargs.get('name'))
        return Article.objects.filter(subscription_name=subscriptions).order_by('-published')
