# -*- coding: utf-8 -*-

from io import BytesIO

from django.test import Client
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from api.views import add_entry, delete_entry, index
from api.models import Entry


class TestViews(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.password = '123'

        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        self.client = Client()

    def test_add_view(self):
        # Test good data
        data = {'new_url': 'https://google.com/', 'new_desc': 'Test 1', 'ttl': '1'}
        resp = self.client.post('/add/', data)
        self.assertEqual(resp.status_code, 302)

        # Let's authenticate
        is_authenticated = self.client.login(username=self.username, password=self.password)
        self.assertTrue(is_authenticated)

        resp = self.client.post('/add/', data)
        self.assertRedirects(resp, '/')
        self.assertEqual(Entry.objects.count(), 1)

        # Test with malformed image
        self.assertEqual(Entry.objects.count(), 1)
        bad_data = {'new_url': '', 'new_desc': 123, 'ttl': '33', 'new_img': BytesIO(b'aaaaaaaaaaa')}

        is_authenticated = self.client.login(username=self.username, password=self.password)
        self.assertTrue(is_authenticated)
        self.client.post('/add/', bad_data)
        self.assertEqual(Entry.objects.count(), 1)

        # Test wrong time-to-live
        bad_data = {'new_url': 'https://google.com/', 'new_desc': 'Test 3', 'delete_on': '-1'}
        self.client.post('/add/', bad_data)
        self.assertEqual(Entry.objects.count(), 1)

        # Test empty data
        self.client.post('/add/', {})
        self.assertEqual(Entry.objects.count(), 1)

    def test_delete_view(self):
        entry = Entry.objects.create(url='https://google.com/', desc='Test 1')
        entry.save()
        self.assertEqual(Entry.objects.count(), 1)
        resp = self.client.delete(f'/delete/{entry.id}')
        self.assertRedirects(resp, '/accounts/login/?next=/delete/1')

        is_authenticated = self.client.login(username=self.username, password=self.password)
        self.assertTrue(is_authenticated)
        resp = self.client.delete(f'/delete/{entry.id}')
        self.assertRedirects(resp, '/')

        self.assertEqual(Entry.objects.count(), 0)

    def test_index_view(self):
        test_request = RequestFactory().get('/', HTTP_USER_AGENT=[])
        test_request.user = self.user
        result = index(test_request)
        self.assertTrue(result.status_code == 200)
        self.assertTrue(bool(result.content))
