from django.urls import path
from .views import aggregator, HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('aggregate/', aggregator, name="aggregator")
]
