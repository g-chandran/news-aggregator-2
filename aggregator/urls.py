from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import HomeListView, SubscriptionListView, profile_view, add_profile, remove_profile, SignupView

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


urlpatterns = [
    path('', cache_page(CACHE_TTL)(HomeListView.as_view()), name="home"),
    path('subscription/<str:name>',
         SubscriptionListView.as_view(), name="subscription"),
    path('profile/', profile_view, name='profile'),
    path('add/<int:id>', add_profile, name='add-profile'),
    path('remove/<int:id>', remove_profile, name='remove-profile'),
    path('signup/', SignupView.as_view(), name="signup")
]
