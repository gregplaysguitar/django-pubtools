# from datetime import date

from django.test import TestCase, Client
from django.contrib.auth.models import User
from pubtools.models import STATUS_FLAG
from .models import Article


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
