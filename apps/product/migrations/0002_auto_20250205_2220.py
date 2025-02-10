# Generated by Django 3.2.25 on 2025-02-05 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['public_id'], name='product_pro_public__f11649_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='product_pro_name_b60cd1_idx'),
        ),
    ]
