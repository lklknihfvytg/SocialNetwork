# Generated by Django 4.1.7 on 2023-04-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='post',
            name='is_tiny',
            field=models.BooleanField(default=False),
        ),
    ]