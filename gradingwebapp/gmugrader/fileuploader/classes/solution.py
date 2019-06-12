from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from decimal import Decimal


from django.conf import settings
from django.db.models import Count, Avg, Max, Min
from .assignment import Assignment
from django.contrib.auth.models import User
from ..helpers.file_operations import get_upload_file_name



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
