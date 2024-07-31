from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from decimal import Decimal


from django.conf import settings
from django.db.models import Count, Avg, Max, Min
import uuid
from ..helpers.file_operations import get_upload_file_name
from django.contrib.auth.models import User
from .course import Course


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
    hidden_status   = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

#best_score      = models.DecimalField (max_digits=5, decimal_places=2, default = Decimal (-1.0))
    num_subs_per_day = models.IntegerField (default=5)
    ACCURACY = 'AC'
    F1SCORE  = 'F1'
    VMEASURE = 'V1'
    ROCSCORE = 'RC'
    OTHER    = 'OT'
    RMSE     = 'RE'
    SCORING_CHOICES = (
        (ACCURACY, 'Accuracy'),
        (F1SCORE, 'F1-Score'),
        (VMEASURE, 'V-measure'),
        (RMSE, 'rmse'),
        (ROCSCORE, 'RC'),
        (OTHER, 'Other'),
    )
    scoring_method = models.CharField (max_length=2, choices=SCORING_CHOICES, default=ACCURACY)

    def __unicode__(self):
        return self.name

