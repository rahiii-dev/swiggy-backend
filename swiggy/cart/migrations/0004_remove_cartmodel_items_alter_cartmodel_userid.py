# Generated by Django 4.1.2 on 2023-02-26 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmodel',
            name='items',
        ),
        migrations.AlterField(
            model_name='cartmodel',
            name='userid',
            field=models.CharField(max_length=300, null=True, unique=True, verbose_name='Userid'),
        ),
    ]
