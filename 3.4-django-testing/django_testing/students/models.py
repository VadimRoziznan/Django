
from django.db import models


class Student(models.Model):

    name = models.TextField(unique=True)

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField(unique=True)

    students = models.ManyToManyField(
        Student,
        blank=True,
        related_name='student',
    )
