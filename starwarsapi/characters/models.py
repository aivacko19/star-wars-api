from operator import mod
from django.db import models
from datetime import datetime
import uuid


class Collection(models.Model):
    filename = models.CharField(max_length=48)
    name = models.CharField(max_length=48)
    created_at = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return f"/collections/{self.filename}/"
