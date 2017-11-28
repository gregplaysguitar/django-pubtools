try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from pubtools.models import AbstractPublishableModel


@python_2_unicode_compatible
class Article(AbstractPublishableModel):
    def get_absolute_url(self):
        return reverse('article', args=(self.id, ))

    def __str__(self):
        return str(self.id)
