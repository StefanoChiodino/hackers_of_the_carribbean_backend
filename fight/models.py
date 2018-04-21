import uuid

from django.db import models


class Comeback(models.Model):
    # id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    comeback_text = models.CharField(max_length=1000)


class Insult(models.Model):
    # id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    insult_text = models.CharField(max_length=1000)
    correct_comeback = models.ForeignKey(Comeback, on_delete=models.CASCADE)


class Step(models.Model):
    index = models.IntegerField(unique=True)
    insult = models.ForeignKey(Insult, on_delete=models.CASCADE)


class Fight(models.Model):
    # id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    current_fight = models.ForeignKey(Step, on_delete=models.CASCADE, null=True)


class Game(models.Model):
    # id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    health = models.IntegerField()
    current_fight = models.ForeignKey(Fight, on_delete=models.CASCADE, null=True)
