from django.http import HttpRequest


def is_client_on_mobile(request: HttpRequest) -> bool:
    return request is not None and hasattr(request, 'META') and 'Android' in request.META.get('HTTP_USER_AGENT', [])
