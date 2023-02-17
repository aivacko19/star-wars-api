from operator import mod
from django.db import models
from datetime import datetime


class Collection(models.Model):
    filename = models.CharField(max_length=48)
    created_at = models.DateTimeField(default=datetime.now)
