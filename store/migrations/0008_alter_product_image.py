# Generated by Django 4.0.1 on 2023-06-13 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/placeolder.png', null=True, upload_to=''),
        ),
    ]