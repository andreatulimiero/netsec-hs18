from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    key = models.CharField(max_length=64, unique=True)
    pwd  = models.TextField(max_length=128)
