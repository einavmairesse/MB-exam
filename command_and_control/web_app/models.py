from django.db import models


class Instances(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField()


class Tests(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=15)
    number_of_instances = models.PositiveIntegerField()
    created_at = models.DateTimeField()


class InstancesTests(models.Model):
    test_name = models.CharField(max_length=200)
    instance_name = models.CharField(max_length=200)
    process_id = models.PositiveIntegerField(default=None, null=True, blank=True)
