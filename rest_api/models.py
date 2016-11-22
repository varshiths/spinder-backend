from django.contrib.auth.models import User
from django.db import models
from math import exp


class Sport(models.Model):
    name = models.CharField(max_length=30)
    no_of_players = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class SUser(User):
    interests = models.ManyToManyField(Sport, blank=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    enthu_level = models.IntegerField(null=True, default=0)
    expertise_level = models.IntegerField(null=True, default=0)
    play_time = models.IntegerField(null=True, default=0)
    rating = models.FloatField(null=True, default=0)
    score = models.FloatField(null=True, default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        score = ((exp(self.rating/10.0)*self.play_time/4 + 2*self.expertise_level + self.enthu_level/5)-2)*10/12.78
        super(SUser, self).save()
