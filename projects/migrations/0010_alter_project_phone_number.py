# Generated by Django 5.0.6 on 2024-07-15 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_project_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
