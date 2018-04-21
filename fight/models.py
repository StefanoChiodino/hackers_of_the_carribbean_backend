import uuid

from django.db import models


class Comeback(models.Model):
    comeback_text = models.CharField(max_length=1000)


class Insult(models.Model):
    insult_text = models.CharField(max_length=1000)
    correct_comeback = models.ForeignKey(Comeback, on_delete=models.CASCADE)


class Fight(models.Model):
    pass


class Step(models.Model):
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE)
    index = models.IntegerField()
    insult = models.ForeignKey(Insult, on_delete=models.CASCADE)


class Game(models.Model):
    health = models.IntegerField()
    current_fight = models.ForeignKey(Fight, on_delete=models.CASCADE, null=True)
