# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.models import AuthLog
import datetime
from api.management.commands.clean_up_auth_log import Command
from api.tests import create_post_request


class TestAuthLog(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('123')
        self.user.save()

    def test_log_cleanup(self):
        for i in range(1, 11):
            AuthLog.objects.create(remote_address='127.0.0.1', attempt_date=datetime.datetime(2019, 11, i))
        AuthLog.objects.create(remote_address='127.0.0.1')  # This one must stay after cleanup

        self.assertEqual(AuthLog.objects.count(), 11)

        c = Command()
        c.handle()
        self.assertEqual(AuthLog.objects.count(), 1)

    def test_brute_login(self):
        request = create_post_request('add/', {}, self.user)

        check = authenticate(request, username='test_user', password='123')
        self.assertTrue(check)

        for i in range(5):
            authenticate(request, username='test_user', password=i)

        check = authenticate(request, username='test_user', password='123')
        self.assertIsNone(check)
