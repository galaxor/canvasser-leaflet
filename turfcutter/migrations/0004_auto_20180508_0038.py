# Generated by Django 2.0.4 on 2018-05-08 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turfcutter', '0003_canvassector_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canvassector',
            name='canvas_area',
        ),
        migrations.AddField(
            model_name='canvassector',
            name='canvas',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='turfcutter.Canvas'),
            preserve_default=False,
        ),
    ]