# Generated by Django 4.1.7 on 2023-04-29 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_photo_delete_car_delete_zavod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='avatar/default.jpg', upload_to='avatar'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='avatar/default.jpg', upload_to='avatar'),
        ),
    ]
