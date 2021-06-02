from django.urls import path
from .views import aggregator, HomeListView, SubscriptionListView

urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('aggregate/', aggregator, name="aggregator"),
    path('subscription/<str:name>',
         SubscriptionListView.as_view(), name="subscription"),
]
