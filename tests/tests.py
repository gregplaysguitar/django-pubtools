from datetime import date, timedelta

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import admin
from pubtools.models import STATUS_FLAG
from .models import Article
from .admin import ArticleAdmin


USERNAME = 'test'
PASSWORD = 'test'


class PubtoolsTestCase(TestCase):
    def setUp(self):
        # add a staff member
        self.user = User(username=USERNAME, is_staff=True)
        self.user.set_password(PASSWORD)
        self.user.save()

    def test_can_access_published(self):
        client = Client()
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_PUBLISHED)
        response = client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_cant_access_draft(self):
        client = Client()
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_DRAFT)
        response = client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_cant_access_preview(self):
        client = Client()
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_PREVIEW)
        response = client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_staff_can_access_preview(self):
        client = Client()
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_PREVIEW)
        client.login(username=USERNAME, password=PASSWORD)
        url = article.get_absolute_url() + \
            '?%s=preview' % (STATUS_FLAG)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_staff_can_access_draft(self):
        client = Client()
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_DRAFT)
        client.login(username=USERNAME, password=PASSWORD)
        url = article.get_absolute_url() + \
            '?%s=draft' % (STATUS_FLAG)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_published_property(self):
        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_DRAFT,
            pub_date=date.today())
        self.assertEqual(article.published, False)

        article.pub_status = Article.PUB_STATUS_PREVIEW
        article.save()
        self.assertEqual(article.published, False)

        article.pub_status = Article.PUB_STATUS_PUBLISHED
        article.save()
        self.assertEqual(article.published, True)

        article.pub_date = date.today() + timedelta(1)
        article.save()
        self.assertEqual(article.published, False)

    def test_ordering(self):
        article_1 = Article.objects.create(
            pub_status=Article.PUB_STATUS_DRAFT,
            pub_date=date.today() - timedelta(3))
        article_2 = Article.objects.create(
            pub_status=Article.PUB_STATUS_PUBLISHED,
            pub_date=date.today() - timedelta(2))
        article_3 = Article.objects.create(
            pub_status=Article.PUB_STATUS_PUBLISHED,
            pub_date=date.today() - timedelta(1))
        article_4 = Article.objects.create(
            pub_status=Article.PUB_STATUS_PUBLISHED,
            pub_date=date.today() + timedelta(1))

        self.assertEqual(Article.objects.all().last(), article_1)
        self.assertEqual(Article.objects.all().first(), article_4)
        self.assertEqual(Article.objects.published().first(), article_3)
        self.assertEqual(article_3.get_next_published(), article_2)
        self.assertEqual(article_2.get_prev_published(), article_3)
        self.assertEqual(article_3.get_prev_published(), None)
        self.assertEqual(article_3.get_next_published(loop=True), article_2)

    def test_admin(self):
        admin_obj = ArticleAdmin(Article, admin.site)

        article = Article.objects.create(pub_status=Article.PUB_STATUS_DRAFT)
        self.assertEqual(admin_obj.view_on_site(article),
                         '/%s?pub_status=draft' % article.id)

        article = Article.objects.create(pub_status=Article.PUB_STATUS_PREVIEW)
        self.assertEqual(admin_obj.view_on_site(article),
                         '/%s?pub_status=preview' % article.id)

        article = Article.objects.create(
            pub_status=Article.PUB_STATUS_PUBLISHED)
        self.assertEqual(admin_obj.view_on_site(article), '/%s' % article.id)
