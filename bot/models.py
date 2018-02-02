from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(null=True, max_length=40)
    state = models.IntegerField(default=0)


class Action(models.Model):
    type_id = models.IntegerField(primary_key=True)
    text = models.TextField()