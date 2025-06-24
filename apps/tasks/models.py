from django.db import models
from apps.dashboard.models import Profile
# Create your models here.
class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estatus = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='id_profile')
    class Meta:
        db_table = 'tasks'