from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = settings.AUTH_USER_MODEL # 'auth.User'

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    timestamp = models.DateTimeField(auto_now_add=True)
    # when ratings occur after a suggestion
    rating_value = models.FloatField(null=True, blank=True)
    did_rate = models.BooleanField(default=False)
    did_rate_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']


