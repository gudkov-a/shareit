# -*- coding: utf-8 -*-

from typing import Optional

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from api.models import AuthLog


class AntiBruteBackend(BaseBackend):
    """
    Prevent site from brute force attacks
    """

    def authenticate(self, request, username=None, password=None):
        remote_addr = self._extract_remote_addr(request)
        if AuthLog.is_host_reached_auth_attempts_limit(remote_addr):
            if settings.DEBUG:
                print('Too many login failures!')
            return None

        user_object = self.get_user_by_username(username)
        if bool(user_object) and self.is_password_valid(user_object, password):
            return user_object

        # Log failure
        AuthLog.objects.create(remote_address=remote_addr)
        return None

    def _extract_remote_addr(self, req: Optional) -> str:
        if req is not None and hasattr(req, 'META'):
            remote_addr = req.META.get('REMOTE_ADDR')
        else:
            remote_addr = '127.0.0.1'
        return remote_addr

    def get_user_by_username(self, username):
        try:
            user = User.objects.get(username=username, is_active=True)
            return user
        except User.DoesNotExist:
            return None

    def is_password_valid(self, user_object, password):
        return user_object.check_password(password)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
