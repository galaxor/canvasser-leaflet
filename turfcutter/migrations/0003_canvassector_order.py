# Generated by Django 2.0.4 on 2018-05-07 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
            ('turfcutter', '0002_auto_20180506_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='canvassector',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
