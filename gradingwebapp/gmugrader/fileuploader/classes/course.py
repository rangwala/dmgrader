from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from decimal import Decimal


from django.conf import settings
from django.db.models import Count, Avg, Max, Min
from django.contrib.auth.models import User

class Course (models.Model): 
    SPRING = 'Spring'
    SUMMER = 'Summer'
    WINTER = 'Winter'
    FALL= 'Fall'
    SEMESTER_CHOICES = (
        (SPRING, 'Spring'), 
        (SUMMER,    'Summer'),
        (WINTER, 'Winter'),
        (FALL, 'Fall')
    ) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="")
    classnum = models.CharField(max_length=5, default="")   
    section = models.CharField(max_length=5, default="")
    year = models.CharField(max_length=4, default="")
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES, default=FALL)
    description = models.CharField(max_length=1000, default="")


    def full_name(self):
        return "%s %s-%s: %s %s (%s. %s)" % (self.name, self.classnum, self.section, self.semester, self.year, self.user.first_name[0], self.user.last_name)

            

