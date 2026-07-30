from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.department_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    register_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.register_number
profile_image = models.ImageField(
    upload_to="profile_images/",
    blank=True,
    null=True
)