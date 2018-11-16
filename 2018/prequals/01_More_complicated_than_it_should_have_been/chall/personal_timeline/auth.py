import jwt
from django.contrib.auth.models import AnonymousUser
from django.middleware.csrf import rotate_token

from personal_timeline.settings import SECRET_KEY


def login(request, user, response):
    if user is None:
        user = request.user

    rotate_token(request)

    token = jwt.encode({'user': user.id, 'admin': user.is_superuser}, SECRET_KEY)
    response.set_cookie('token', token, httponly=True)
    request.user = user


def logout(request, response):
    response.delete_cookie('token')
    request.session.flush()
    request.user = AnonymousUser()
