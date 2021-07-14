from django.db import models

class Horario(models.Model):
    horario = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=True)