from django.urls import path
from .views import HomeListView, SubscriptionListView, profile_view, add_profile, remove_profile, SignupView

urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('subscription/<str:name>',
         SubscriptionListView.as_view(), name="subscription"),
    path('profile/', profile_view, name='profile'),
    path('add/<int:id>', add_profile, name='add-profile'),
    path('remove/<int:id>', remove_profile, name='remove-profile'),
    path('signup/', SignupView.as_view(), name="signup")
]
