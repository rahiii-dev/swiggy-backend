# Generated by Django 4.1.2 on 2023-02-26 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cartmodel_items_alter_cartmodel_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemmodel',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cartmodel'),
        ),
    ]
