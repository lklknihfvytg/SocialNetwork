# Generated by Django 4.1.7 on 2023-04-12 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_zavod_post_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='zavod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='network.zavod'),
        ),
    ]
