from __future__ import unicode_literals

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from decimal import Decimal


from django.conf import settings
from django.db.models import Count, Avg, Max, Min
from ..helpers.file_operations import get_upload_file_name

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    fileshot=models.FileField(upload_to=get_upload_file_name)
    accuracy=models.DecimalField(max_digits=7,decimal_places=2,default=Decimal(0.0))
    #accuracy = get_accuracy_value(fileshot)


