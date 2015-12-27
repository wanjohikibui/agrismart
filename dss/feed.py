from django.contrib.syndication.views import Feed
from .models import Entry


class LatestPosts(Feed):
    title = "News section"
    link = "/feed/"
    description = "Latest News "

    def items(self):
        return Entry.objects.published()[:5]