from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import (
    HomeListView,
    SubscriptionListView,
    profile_view,
    add_profile,
    remove_profile,
    SignupView,
    get_articles_as_CSV,
    ArticleDetailView
)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('subscription/<str:name>',
         SubscriptionListView.as_view(), name="subscription"),
    path('profile/', profile_view, name='profile'),
    path('add/<int:id>', add_profile, name='add-profile'),
    path('remove/<int:id>', remove_profile, name='remove-profile'),
    path('signup/', SignupView.as_view(), name="signup"),
    path('download-articles/', get_articles_as_CSV, name="download-articles"),
    path('article/<int:pk>/', cache_page(CACHE_TTL)
         (ArticleDetailView.as_view()), name="show-article")
]
