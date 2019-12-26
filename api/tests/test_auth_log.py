# -*- coding: utf-8 -*-

from django.test import TestCase
from api.models import AuthLog
import datetime
from api.management.commands.clean_up_auth_log import Command


class TestAuthLog(TestCase):

    def setUp(self):
        for i in range(1, 11):
            AuthLog.objects.create(remote_address='127.0.0.1', attempt_date=datetime.datetime(2019, 11, i))
        AuthLog.objects.create(remote_address='127.0.0.1')  # This one must stay after cleanup

    def test_log_cleanup(self):
        self.assertEqual(AuthLog.objects.count(), 11)

        c = Command()
        c.handle()
        self.assertEqual(AuthLog.objects.count(), 1)
