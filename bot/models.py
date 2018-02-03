from django.db import models

REVIEW_PRICE_ID = 1


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(null=True, max_length=40)
    state = models.IntegerField(default=0)


class Action(models.Model):
    type_id = models.IntegerField(primary_key=True)
    text = models.TextField()


class Price(models.Model):
    value = models.FloatField()