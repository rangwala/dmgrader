from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from time import time

from decimal import Decimal

from django.conf import settings

from django.contrib.auth.models import User

import uuid

from datetime import datetime    

from django.db.models import Count, Avg, Max, Min

#from tinymce.models import HTMLField


def get_upload_file_name(instance,filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

#


# This is the high level view of an Assignment
# Can only be created by an admin
# Some things are viewable by a student
class Assignment (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name            = models.CharField (max_length=200)
    description     = models.TextField()
    ground_truth    = models.FileField(upload_to=get_upload_file_name)
    pub_date        = models.DateTimeField('date  published',auto_now_add=True,blank=True)
    deadline_date   = models.DateTimeField('deadline',blank=True,auto_now_add=False)
    uploaded_cnt    = models.IntegerField(default=0)
    train_data      = models.FileField(upload_to=get_upload_file_name) 
    test_data       = models.FileField(upload_to=get_upload_file_name) 
    format_example  = models.FileField(upload_to=get_upload_file_name) 
    sampling_private=models.IntegerField (default=50) 
    #best_score      = models.DecimalField (max_digits=5, decimal_places=2, default = Decimal (-1.0))

    def __unicode__(self):
        return self.name

class Solution (models.Model):
    assignment      = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    solution_file   = models.FileField(upload_to=get_upload_file_name)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt         = models.IntegerField(default=0)
    score           = models.DecimalField(max_digits=5,decimal_places=2,default=Decimal(-1.0))
    # private_score is above
    public_score    = models.DecimalField(max_digits=5,decimal_places=2,default=Decimal(-1.0))
    submission_time = models.DateTimeField('date submitted',auto_now_add=True,blank=True)
    ERROR = 'ER'
    OK    = 'OK'
    STATUS_CHOICES = (
        (ERROR, 'Error'), 
        (OK,    'Okay'),
    )
    status          = models.CharField (max_length =2, choices=STATUS_CHOICES, default=ERROR)

class UserProfile (models.Model):
    user         = models.OneToOneField (User, on_delete=models.CASCADE)
    tot_attempts = models.IntegerField (default=0)
    team_name    = models.CharField (max_length=200)

# so we need a user registration view to incorporate this




# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    fileshot=models.FileField(upload_to=get_upload_file_name)
    accuracy=models.DecimalField(max_digits=7,decimal_places=2,default=Decimal(0.0))
    #accuracy = get_accuracy_value(fileshot)



# What we need 
# Admin upload a problem SET
# Students upload solution file to comare to the problem SET. 
#

    




