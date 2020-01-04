# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from api.tests import create_post_request
from api.views import add_entry, delete_entry, index
from api.models import Entry
from io import BytesIO


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='123')

    def test_add_view(self):
        # Test good data
        data = {'new_url': 'https://google.com/', 'new_desc': 'Test 1', 'ttl': '1'}
        test_request = create_post_request('add/', data, self.user)
        add_entry(test_request)
        self.assertEqual(Entry.objects.count(), 1)

        # Test with malformed image
        bad_data = {'new_url': '', 'new_desc': 123, 'ttl': '33', 'new_img': BytesIO(b'aaaaaaaaaaa')}
        test_request = create_post_request('add/', bad_data, self.user)
        add_entry(test_request)
        self.assertEqual(Entry.objects.count(), 1)

        # Test wrong time-to-live
        bad_data = {'new_url': 'https://google.com/', 'new_desc': 'Test 3', 'delete_on': '-1'}
        test_request = create_post_request('add/', bad_data, self.user)
        add_entry(test_request)
        self.assertEqual(Entry.objects.count(), 1)

        # Test empty data
        test_request = create_post_request('add/', {}, self.user)
        add_entry(test_request)
        self.assertEqual(Entry.objects.count(), 1)

    def test_delete_view(self):
        data = {'new_url': 'https://google.com/', 'new_desc': 'Test 1', 'ttl': '1'}
        test_request = create_post_request('add/', data, self.user)
        add_entry(test_request)
        self.assertEqual(Entry.objects.count(), 1)

        entry = Entry.objects.all()[0]
        data = {}
        delete_request = create_post_request('add/', data, self.user)
        delete_entry(delete_request, entry.pk)
        self.assertEqual(Entry.objects.count(), 0)

    def test_index_view(self):
        test_request = RequestFactory().get('/', HTTP_USER_AGENT=[])
        test_request.user = self.user
        result = index(test_request)
        self.assertTrue(result.status_code == 200)
        self.assertTrue(bool(result.content))
