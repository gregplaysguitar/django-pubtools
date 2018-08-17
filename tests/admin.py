from django.contrib import admin
from pubtools.admin import PublishableModelAdminMixin

from .models import Article


@admin.register(Article)
class ArticleAdmin(PublishableModelAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'pub_status', )
