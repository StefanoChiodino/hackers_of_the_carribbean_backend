import uuid

from django.db import models


class Comeback(models.Model):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.text)


class Insult(models.Model):
    text = models.CharField(max_length=1000)
    correct_comeback = models.ForeignKey(Comeback, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)


class Fight(models.Model):
    step_index = models.IntegerField(default=0)

    def __str__(self):
        return str(f'{self.current_step}')


class Step(models.Model):
    index = models.IntegerField()
    insult = models.ForeignKey(Insult, on_delete=models.CASCADE)
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.index} - {self.insult}')


class StepComeback(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    comeback = models.ForeignKey(Comeback, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.step} - {self.comeback}')


class Game(models.Model):
    health = models.IntegerField()
    current_fight = models.ForeignKey(Fight, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(f'{self.health} - {self.current_fight}')
