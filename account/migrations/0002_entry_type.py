# Generated by Django 3.2.9 on 2022-01-12 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]