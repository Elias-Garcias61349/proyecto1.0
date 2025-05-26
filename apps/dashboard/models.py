#plantlla del modelo de datos el cual se conectara a la base de datos 
#es la plantilla
from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos')