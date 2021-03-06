# Generated by Django 3.2.5 on 2021-07-23 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='InstancesTests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=200)),
                ('instance_name', models.CharField(max_length=200)),
                ('process_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=15)),
                ('number_of_instances', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]
