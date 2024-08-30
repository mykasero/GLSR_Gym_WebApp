from django.db import models

# Create your models here.

class Test1(models.Model):
    test_name = models.CharField(max_length=50)
    test_age = models.IntegerField()