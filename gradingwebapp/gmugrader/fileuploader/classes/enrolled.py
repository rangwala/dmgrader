from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from decimal import Decimal


from django.conf import settings
from django.db.models import Count, Avg, Max, Min
from django.contrib.auth.models import User
from .course import Course


class Enrolled (models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    course          = models.ForeignKey(Course, on_delete=models.CASCADE)
    active          = models.BooleanField(default=True)
    enrolled_timestamp = models.DateTimeField('date  enrolled', auto_now_add=True,blank=True)