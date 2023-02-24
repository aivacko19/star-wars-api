from operator import mod
from django.db import models
from datetime import datetime
import uuid


class Collection(models.Model):
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=48)
    created_at = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return f"/collections/{self.uuid}/"
