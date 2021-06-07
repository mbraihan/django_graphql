from django.db import models
import uuid

# Create your models here.

class Employee(models.Model):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    employee_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length = 100, null = False, blank = False)
    middle_name = models.CharField(max_length = 100, null = False, blank = False)
    last_name = models.CharField(max_length = 100, null = False, blank = False)
    gender = models.CharField(max_length = 15, choices = GENDER_CHOICE, default = 'm')
    address = models.CharField(max_length = 255, default = '')
    salary = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, blank = False, null = False)

    def __str__(self):
        return self.first_name, self.last_name, self.middle_name, self.address

    class Meta:
        ordering = ('first_name', 'salary', )

class Sector(models.Model):
    sector_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255, null = False, blank = False)
    location = models.CharField(max_length = 255, null = False, blank = False)

    def __str__(self):
        return self.name, self.location

    class Meta:
        ordering = ('name', )

class Project(models.Model):
    project_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255, null = False, blank = False)
    location = models.CharField(max_length = 255, null = False, blank = False)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name, self.location

    class Meta:
        ordering = ('name', )


class Actor(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )

class Movie(models.Model):
    title = models.CharField(max_length = 100)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )