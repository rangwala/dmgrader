from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from time import time

from decimal import Decimal

from django.conf import settings

from django.contrib.auth.models import User

import uuid

import sys

from datetime import datetime    

from django.db.models import Count, Avg, Max, Min

from .classes.article import Article
from .classes.solution import Solution
from .classes.assignment import Assignment
from .classes.course import Course
from .classes.enrolled import Enrolled
from .helpers.file_operations import get_upload_file_name

#from tinymce.models import HTMLField
def get_courses(self):
    coursesString = ""
    enrollments = Enrolled.objects.filter(user_id=self.id).values_list("course_id", flat=True)
    courses = Course.objects.filter(id__in=enrollments)
    for course in courses:
        coursesString += course.full_name()
        coursesString += "\n"
    return coursesString

User.add_to_class("get_courses", get_courses)



'''
class UserProfile (models.Model):
    user         = models.OneToOneField (User, on_delete=models.CASCADE, related_name='profile')
    class_name   = models.IntegerField(default=0)
'''
# so we need a user registration view to incorporate this





# What we need 
# Admin upload a problem SET
# Students upload solution file to comare to the problem SET. 
#

    




