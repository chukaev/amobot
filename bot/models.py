from django.db import models

REVIEW_PRICE_ID = 1


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(null=True, max_length=40)
    first_name = models.CharField(max_length=50)
    state = models.IntegerField(default=0)
    api_postfix = models.IntegerField(default=0)


class TypeAction(models.Model):
    action_id = models.CharField(unique=True, max_length=40)
    text = models.TextField()


class ProblemAction(models.Model):
    action_id = models.CharField(unique=True, max_length=40)
    text = models.TextField()


class Price(models.Model):
    value = models.FloatField()