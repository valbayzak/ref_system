# Generated by Django 3.2.4 on 2021-06-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'ACTIVE'), (2, 'NOT_ACTIVE'), (3, 'ACCEPTED')], default=1, verbose_name='Статус'),
        ),
    ]