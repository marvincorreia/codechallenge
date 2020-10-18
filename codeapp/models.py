from django.db import models


# Create your models here.

class CodeModel(models.Model):
    code = models.TextField(null=True, blank=True)
