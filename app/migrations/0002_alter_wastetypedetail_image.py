# Generated by Django 5.0.1 on 2024-02-05 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wastetypedetail',
            name='image',
            field=models.CharField(default='', max_length=400),
        ),
    ]