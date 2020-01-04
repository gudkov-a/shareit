# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from api.models import AuthLog
from django.conf import settings


class AntiBruteBackend:
    """
    Prevent site from brute force attacks
    """

    def authenticate(self, request, username=None, password=None):
        remote_addr = request.META.get('REMOTE_ADDR')
        num_of_attempts = AuthLog.get_attempts_by_ip_address(remote_addr)
        if num_of_attempts > settings.ATTEMPTS_TO_LOGIN - 1:
            if settings.DEBUG:
                print('Too many login failures!')
            return None

        user_object = self.get_user_by_username(username)
        if bool(user_object) and self.is_password_valid(user_object, password):
            return user_object

        # Log failure
        AuthLog.objects.create(remote_address=remote_addr)
        return None

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
