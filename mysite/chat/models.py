from django.db import models

# Create your models here.
class Author(models.Model):
    id_str = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
