# Generated by Django 4.1.7 on 2023-04-12 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.CharField(default='/home/user/Документы/Django/SocialNetwork/static/img/avatar/default.jpg', max_length=128),
        ),
    ]
