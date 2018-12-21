from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User,
            on_delete=models.CASCADE)
    balance = models.IntegerField()
    clear_password = models.CharField(max_length=128)
