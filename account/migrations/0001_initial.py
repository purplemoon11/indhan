# Generated by Django 3.2.9 on 2021-12-12 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('Gasoline_type', models.CharField(max_length=20, null=True)),
                ('Gasoline', models.CharField(max_length=20, null=True)),
                ('date', models.CharField(max_length=20)),
                ('vehicle_number', models.CharField(max_length=20, null=True)),
                ('purpose', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'entry',
            },
        ),
    ]