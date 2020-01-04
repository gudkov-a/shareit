# -*- coding: utf-8 -*-

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.session import SessionStorage


def create_post_request(url, data, user):
    test_request = RequestFactory().post(url, data)
    test_request.user = user

    # RequestFactory does'n support session, so I need to fix this
    middleware = SessionMiddleware()
    middleware.process_request(test_request)
    test_request.session.save()

    messages = SessionStorage(test_request)
    setattr(test_request, '_messages', messages)

    # Also create META attribute
    content_type = "multipart/form-data; boundary=------------------------1493314174182091246926147632"
    setattr(test_request, 'META', dict([('REMOTE_ADDR', '127.0.0.1'), ('CONTENT_TYPE', content_type)]))

    return test_request
