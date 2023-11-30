from django.urls import path
from .apps import ChurchConfig

from .views import *

app_name = ChurchConfig.name

urlpatterns = [
    path("category/<str:slug>", CategoryView.as_view(), name="category"),
    path("tag/<str:slug>", TagView.as_view(), name="tag"),
    path("sermons", SermonsView.as_view(), name="sermons"),
    path("event/<str:slug>", EventView.as_view(), name="event"),
    path("events", EventsListView.as_view(), name="events"),
    path("single-blog", SingleBlogView.as_view(), name="single-blog"),
    path("blog", BlogView.as_view(), name="blog"),
    path("post/<str:slug>", PostView.as_view(), name="post"),
    path("about", AboutView.as_view(), name="about"),
    path("contact", ContactView.as_view(), name="contact"),
    path("", HomeView.as_view(), name="home"),
]