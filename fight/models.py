import uuid

from django.db import models


class Comeback(models.Model):
    comeback_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    comeback_text = models.CharField(max_length=1000)


class Insult(models.Model):
    insult_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    insult_text = models.CharField(max_length=1000)
    correct_comeback_id = models.ForeignKey(Comeback, on_delete=models.CASCADE)


class Step(models.Model):
    index = models.IntegerField(primary_key=True)
    insult_id = models.ForeignKey(Insult, on_delete=models.CASCADE)


class Fight(models.Model):
    fight_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    current_fight = models.ForeignKey(Step, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fight_id)


class Game(models.Model):
    game_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    health = models.IntegerField()
    current_fight = models.ForeignKey(Fight, on_delete=models.CASCADE)
