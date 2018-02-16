from django.db import models

REVIEW_PRICE_ID = 1


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(null=True, max_length=40)
    first_name = models.CharField(max_length=50)
    state = models.IntegerField(default=1)
    api_postfix = models.IntegerField(default=0)
    username = models.CharField(max_length=50, default='Пусто')
    city = models.CharField(max_length=50, default='Москва')
    country = models.CharField(max_length=20, default='Россия')
    lead_id = models.CharField(max_length=20, null=True)
    send_review = models.BooleanField(default=True)


class TypeAction(models.Model):
    action_id = models.CharField(unique=True, max_length=40)
    text = models.TextField()


class ProblemAction(models.Model):
    action_id = models.CharField(unique=True, max_length=40)
    text = models.TextField()


class Price(models.Model):
    value = models.FloatField()


class Question(models.Model):
    text = models.TextField()
