# Generated by Django 2.0.3 on 2018-04-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='imageuser',
            field=models.ImageField(upload_to='imageinst', verbose_name='photouser'),
        ),
    ]