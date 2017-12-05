django-pubtools is a helper library for creating publishable django models.

[![Circle CI](https://circleci.com/gh/gregplaysguitar/django-pubtools.svg?style=svg)](https://circleci.com/gh/gregplaysguitar/django-pubtools)
[![codecov](https://codecov.io/gh/gregplaysguitar/django-pubtools/branch/master/graph/badge.svg)](https://codecov.io/gh/gregplaysguitar/django-pubtools)
[![Latest Version](https://img.shields.io/pypi/v/django-pubtools.svg?style=flat)](https://pypi.python.org/pypi/django-pubtools/)

## Overview

Extend the `AbstractPublishableModel` class to create a publishable model class.

- Publishable content can be in either draft, preview, or published status.
- Draft content may be previewed on the site by a logged-in staff member
- Preview content may be previewed publicly, via a special url


## Installation

    pip install django-pubtools


## Example implementation

models.py:

```python
from django.db import models
import pubtools.models

class Article(pubtools.models.AbstractPublishableModel):
    title = models.CharField(max_length=100)
```

views.py:

```python
from django.http import HttpResponse
from .models import Article

def article(request, id):
    # pass the request to enable staff preview
    articles = Article.objects.published(request)
    article = articles.get(id=id)
    return HttpResponse(article.title)
```

admin.py:

```python
from django.contrib import admin
from baseclasses.admin import PublishableModelAdminMixin

from .models import Article

@admin.register(Article)
class ArticleAdmin(PublishableModelAdminMixin, admin.ModelAdmin):
    list_display = ['title']
```

## Reference

### `pubtools.models.AbstractPublishableModel`

##### Model fields

- `created` (datetime, set on creation)
- `last_updated` (datetime, updated on save)
- `pub_date` (date)
- `pub_status` (one of draft, review or published)

##### Model methods

- `published` (property) return True if the instance is published
- `get_prev_published(qs=None, loop=False)` get previous published instance
- `get_next_published(qs=None, loop=False)` get next published instance

### `pubtools.models.PublishableModelQuerySet`

##### Manager/queryset methods

- `published(self, request=None)` If request is passed, and a preview status
  flag is in request.GET, then check if the user is a staff member, and
  return objects with the requested status if so. Otherwise, return only
  published objects.

### `pubtools.admin.PublishableModelAdminMixin`

- Overrides `view_on_site` to add a flag to urls for draft/preview content.
- Adds a "Publish selected" action to the admin
