from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    author = models.ForeignKey(User, null=False)
    message = models.TextField(blank=True)
    posted = models.DateTimeField(auto_now_add=True)
