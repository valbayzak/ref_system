from django.db import models
from oper.models import Invite
# Create your models here.



class User(models.Model):
    phone = models.CharField("Номер телефона", max_length=20)

    def __str__(self):
        return self.phone