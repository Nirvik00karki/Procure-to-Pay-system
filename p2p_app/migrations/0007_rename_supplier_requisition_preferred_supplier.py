# Generated by Django 5.0.4 on 2024-05-15 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p2p_app', '0006_requisition_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requisition',
            old_name='supplier',
            new_name='preferred_supplier',
        ),
    ]