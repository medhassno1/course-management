from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(default="")
