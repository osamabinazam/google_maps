from django.db import models

# Create your models here.

class User(models.Model):
    f_name = models.CharField(max_length=50 )
    l_name = models.CharField(max_length=50)
    latitude= models.FloatField()
    longitude = models.FloatField()

    # String Representation of the model
    def __str__(self):
        return f"{self.f_name} {self.l_name}"
