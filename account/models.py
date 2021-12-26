from django.db import models

# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=20, null=True)
    Gasoline_type = models.CharField(max_length=20, null=True)
    Gasoline = models.CharField(max_length=20, null=True)
    date = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20, null=True)
    purpose = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'entry'
