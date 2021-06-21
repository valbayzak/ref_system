from datetime import datetime

from django.db import models

# Create your models here.

CHOICE_STATUS = [
    (1, 'ACTIVE'),
    (2, 'NOT_ACTIVE'),
    (3, 'ACCEPTED'),
]


class Subscriber(models.Model):
    phone = models.CharField("Номер телефона", max_length=20)
    active = models.BooleanField(default=True)
    add_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone


class Invite(models.Model):
    sender_subs_id = models.ForeignKey(Subscriber, verbose_name="Отправитель", on_delete=models.DO_NOTHING)
    receiver_subs_id = models.ForeignKey(Subscriber, verbose_name="Получатель", related_name="receiver_subs",
                                         on_delete=models.DO_NOTHING)
    status = models.PositiveSmallIntegerField("Статус", choices=CHOICE_STATUS, default=1)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=datetime(9999, 12, 31, 23, 59, 59))

    def __str__(self):
        return f'Отправитель: {self.sender_subs_id} | Получатель: {self.receiver_subs_id}'
