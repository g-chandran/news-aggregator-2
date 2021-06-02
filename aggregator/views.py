from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Subscription, Profile, Article
from .aggregator import aggregator


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "signup.html"


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


@login_required
def profile_view(request):
    aggregator.delay()
    print("Crossed aggregator")
    subscriptions = Subscription.objects.all()
    current_user_profile = Profile.objects.filter(name=request.user)
    current_user_subscriptions = [
        sub.subscription.name for sub in current_user_profile]
    context = {'subscriptions': subscriptions,
               'current_subscriptions': current_user_subscriptions}
    return render(request, 'profile.html', context)


@login_required
def add_profile(request, id):
    requested_subscription = get_object_or_404(Subscription, id=id)
    subscriptions = Subscription.objects.all()
    p = Profile.objects.create(
        name=request.user, subscription=requested_subscription)
    p.save()
    current_user_profile = Profile.objects.filter(name=request.user)
    current_user_subscriptions = [
        sub.subscription.name for sub in current_user_profile]
    context = {'subscriptions': subscriptions,
               'current_subscriptions': current_user_subscriptions}
    return render(request, 'profile.html', context)


@login_required
def remove_profile(request, id):
    requested_subscription = get_object_or_404(Subscription, id=id)
    subscriptions = Subscription.objects.all()
    Profile.objects.filter(
        name=request.user, subscription=requested_subscription).delete()
    current_user_profile = Profile.objects.filter(name=request.user)
    current_user_subscriptions = [
        sub.subscription.name for sub in current_user_profile]
    context = {'subscriptions': subscriptions,
               'current_subscriptions': current_user_subscriptions}
    return render(request, 'profile.html', context)
