# Generated by Django 4.2 on 2023-04-29 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
