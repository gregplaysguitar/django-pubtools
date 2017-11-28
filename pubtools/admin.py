from .models import STATUS_FLAG


class PublishableModelAdminMixin(object):
    """Enables staff preview of non-published objects, in combination with
       PublishableModelQuerySet.published(request). Note the view must pass a
       request to this method or the preview won't work, and the mixin needs to
       come before admin.ModelAdmin in the parent classes. Requires Django 1.7.
    """

    actions = ('publish_selected', )
    list_editable = ('pub_status', )

    def publish_selected(self, request, qs):
        qs.update(pub_status=self.model.PUB_STATUS_PUBLISHED)

    def view_on_site(self, obj):
        url = obj.get_absolute_url()
        if not obj.published:
            if obj.pub_status == obj.PUB_STATUS_PREVIEW:
                status = 'preview'
            else:
                status = 'draft'
            prefix = '&' if url.find('?') != -1 else '?'
            return '%s%s%s=%s' % (url, prefix, STATUS_FLAG, status)
        return url
