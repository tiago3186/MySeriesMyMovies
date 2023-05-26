from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    average_rating = models.FloatField()
    user_rating = models.FloatField()

    def __str__(self):
        return self.title
