from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView

from church.models import Advantage, SiteSettings, Sermon, Event, Donate, Post, Pastor


# Create your views here.


class HomeView(TemplateView):
    template_name = "church/index-home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSettings.load()
        advantage = Advantage.objects.all()[:site_settings.advantage_max_count]
        if advantage.count() > 0:
            context['advantages'] = advantage
            context['advantage_col'] = int(abs(12 / advantage.count()))
        sermon = Sermon.objects.filter(deleted=False,pin=True).order_by('pin', '-created_at')
        if sermon.count() > 0:
            context['sermon_today'] = sermon.first
        events = Event.objects.filter(deleted=False).order_by('datatime_event')
        if events.count() > 0:
            context['events'] = events[:site_settings.event_max_count]
        donate = Donate.objects.filter(deleted=False).first()
        if donate:
            context['donate'] = donate
        news = Post.objects.all()[:site_settings.news_post_max_count]
        if news.count() > 0:
            context['news'] = news
            context['news_col'] = int(abs(12 / news.count()))
        return context


class ContactView(TemplateView):
    template_name = "church/contact.html"


class AboutView(TemplateView):
    template_name = "church/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pastors = Pastor.objects.all()
        if pastors.count() > 0:
            context['pastors'] = pastors
        context['title'] = _('About Us')
        return context


class SingleBlogView(TemplateView):
    template_name = "church/single-blog.html"


class BlogView(ListView):
    template_name = "church/blog.html"
    context_object_name = "news"
    paginate_by = 6
    allow_empty = False
    def get_queryset(self):
         self.news = Post.objects.filter(deleted=False).order_by('-created_at')
         return self.news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Blog')
        return context


class EventsListView(ListView):
    template_name = "church/events-list.html"
    context_object_name = "events"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Event.objects.filter(deleted=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Event List')
        return context

class EventView(DetailView):
    model = Event
    template_name = 'church/event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SermonsView(ListView):
    template_name = "church/sermons.html"
    context_object_name = "sermons"
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        self.sermon_pin = Sermon.objects.filter(deleted=False,pin=True).order_by('-created_at').first()
        sermons = Sermon.objects.filter(deleted=False).order_by('-data_sermon')
        if self.sermon_pin:
            return sermons.exclude(pk=self.sermon_pin.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.sermon_pin:
            context['sermon_today'] = self.sermon_pin
        context['title'] = _('Sermons')
        return context
