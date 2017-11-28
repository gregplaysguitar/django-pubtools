from django.contrib import admin
from pubtools.admin import PublishableModelAdminMixin

from .models import Article


@admin.register(Article)
class ArticleAdmin(PublishableModelAdminMixin, admin.ModelAdmin):
    pass
