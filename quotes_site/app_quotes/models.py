from django.db import models

# Create your models here.

class Quote(models.Model):
    text = models.TextField(blank=True)
    source = models.CharField(max_length=128)
    weight = models.PositiveIntegerField(default=1)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)