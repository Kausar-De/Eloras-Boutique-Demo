# Generated by Django 4.0.1 on 2023-06-10 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colour',
            field=models.TextField(choices=[('Orange', 'Orange'), ('Brown', 'Brown'), ('Black', 'Black'), ('Green', 'Green'), ('Blue', 'Blue'), ('Pink', 'Pink'), ('Red', 'Red'), ('Yellow', 'Yellow'), ('Gray', 'Gray'), ('White', 'White')], default='Choose Colour...', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.TextField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('U', 'U')], default='Choose Size...', max_length=200),
        ),
    ]