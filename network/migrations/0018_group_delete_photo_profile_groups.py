# Generated by Django 4.1.7 on 2023-05-04 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0017_alter_profile_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=45)),
                ('about', models.CharField(blank=True, max_length=128)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('profile_pic', models.ImageField(default='avatar/default.jpg', upload_to='avatar')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_admin', to=settings.AUTH_USER_MODEL, verbose_name='admin')),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_groups', to='network.group'),
        ),
    ]
