# coding: utf-8

import datetime

from django.db import models

from next_prev import next_or_prev_in_order


STATUS_FLAG = 'pub_status'


class PublishableModelQuerySet(models.QuerySet):
    def published(self, request=None):
        """If request is passed, and a preview flag is in request.GET,
           then check if the user is a staff member, and return all objects
           if so. Otherwise, return only published objects.
        """

        # Note, django doesn't allow view caching on any request that accesses
        # request.user, so this must ONLY happen if the preview flag is
        # present. Otherwise, the view can never be cached.

        status = request.GET.get(STATUS_FLAG) if request else None

        # show all to staff members
        if status == 'draft' and request.user.is_staff:
            return self

        # previews are publicly visible with the url flag
        if status == 'preview':
            return self.filter(
                pub_status__gte=AbstractPublishableModel.PUB_STATUS_PREVIEW)

        # otherwise, published only
        return self.filter(
            pub_status=AbstractPublishableModel.PUB_STATUS_PUBLISHED,
            pub_date__lte=datetime.datetime.now())


class AbstractPublishableModel(models.Model):
    """Custom publication logic for mmoser content models. """

    PUB_STATUS_DRAFT = 10
    PUB_STATUS_PREVIEW = 20
    PUB_STATUS_PUBLISHED = 30
    PUB_STATUS_CHOICES = (
        (PUB_STATUS_DRAFT, 'Draft'),
        (PUB_STATUS_PREVIEW, 'Preview'),
        (PUB_STATUS_PUBLISHED, 'Published'),
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    pub_date = models.DateField(u'publication date', db_index=True,
                                default=datetime.date.today)
    pub_status = models.PositiveSmallIntegerField(
        choices=PUB_STATUS_CHOICES, default=0, db_index=True)

    objects = PublishableModelQuerySet.as_manager()

    @property
    def published(self):
        return self.pub_status == self.PUB_STATUS_PUBLISHED and \
            self.pub_date <= datetime.date.today()

    class Meta:
        abstract = True
        ordering = ('-pub_date', '-created',)

    def get_prev_published(self, loop=False):
        qs = self.__class__.objects.published()
        return next_or_prev_in_order(self, qs=qs, prev=True, loop=loop)

    def get_next_published(self, loop=False):
        qs = self.__class__.objects.published()
        return next_or_prev_in_order(self, qs=qs, prev=False, loop=loop)
