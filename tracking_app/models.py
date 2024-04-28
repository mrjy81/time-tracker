from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()


class TrackerTitles(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class TrackerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(TrackerTitles, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    total_minutes = models.PositiveIntegerField(default=0)
    paused_at = jmodels.jDateTimeField(null=True, blank=True)
    is_stopped = models.BooleanField(default=True)
    datetime = jmodels.jDateTimeField()

    def __str__(self):
        return str(self.title)
