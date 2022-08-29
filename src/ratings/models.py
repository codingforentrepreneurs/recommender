from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = settings.AUTH_USER_MODEL # 'auth.User'

# user_obj = User.objects.first()
# user_ratings = user_obj.rating_set.all()

# rating_obj = Rating.objects.first()
# user_obj = rating_obj.user
# user_ratings = user_obj.rating_set.all()

class RatingChoice(models.IntegerChoices):
    ONE = 1 
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = 'Rate this'
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoice.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)