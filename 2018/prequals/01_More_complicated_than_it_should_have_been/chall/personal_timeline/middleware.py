import jwt
from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from jwt import DecodeError
from jwt.exceptions import InvalidKeyError

from personal_timeline.settings import SECRET_KEY


def get_user(request):
    if 'token' not in request.COOKIES:
        request._cached_user = AnonymousUser()
    if not hasattr(request, '_cached_user'):
        try:
            try:
                token = jwt.decode(request.COOKIES['token'], SECRET_KEY)
            except InvalidKeyError:
                token = jwt.decode(request.COOKIES['token'], None, False)  # TODO: debug only, remove it before production
            user = User.objects.get(pk=token['user'])
            user.is_superuser = token['admin']
            request._cached_user = user
        except (DecodeError, User.DoesNotExist):
            request._cached_user = AnonymousUser()
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
