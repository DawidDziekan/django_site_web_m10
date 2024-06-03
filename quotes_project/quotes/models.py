from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    born_date = models.CharField(max_length=100, null=True, blank=True)
    born_location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.text[:50]

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
