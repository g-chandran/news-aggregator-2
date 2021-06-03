from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    name = models.CharField(max_length=30)
    thumbnail = models.URLField()
    last_updated = models.DateTimeField()
    site_url = models.URLField()
    feed_url = models.URLField()

    def __str__(self):
        return self.name


class Article(models.Model):
    subscription_name = models.ForeignKey(
        to=Subscription, on_delete=models.CASCADE)
    published = models.DateTimeField()
    title = models.CharField(max_length=300)
    author = models.CharField(default=' ', max_length=100)
    summary = models.CharField(default=' ', max_length=500)
    media = models.URLField()
    article_id = models.CharField(max_length=200, unique=True)
    article_link = models.URLField()
    article = models.CharField(max_length=50000)

    def __str__(self):
        return f"{self.subscription_name.name}: {self.title}"


class Profile(models.Model):
    name = models.ForeignKey(to=User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        to=Subscription, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name.username} - {self.subscription.name}"
