# Generated by Django 3.2.3 on 2021-06-01 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('thumbnail', models.URLField()),
                ('last_updated', models.DateTimeField()),
                ('site_url', models.URLField()),
                ('feed_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.DateTimeField()),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(default=' ', max_length=100)),
                ('summary', models.CharField(default=' ', max_length=500)),
                ('media', models.URLField()),
                ('article_id', models.CharField(max_length=200, unique=True)),
                ('article_link', models.URLField()),
                ('subscription_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.subscription')),
            ],
        ),
    ]