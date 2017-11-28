from django.urls import reverse

from pubtools.models import AbstractPublishableModel


class Article(AbstractPublishableModel):
    def get_absolute_url(self):
        return reverse('article', args=(self.id, ))
