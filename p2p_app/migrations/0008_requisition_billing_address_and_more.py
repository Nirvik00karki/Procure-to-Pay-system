# Generated by Django 5.0.4 on 2024-05-15 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2p_app', '0007_rename_supplier_requisition_preferred_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='billing_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='requisition',
            name='payment_method',
            field=models.CharField(default='e.g.Cash', max_length=50),
        ),
        migrations.AddField(
            model_name='requisition',
            name='shipping_address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
