from random import randint, random

from django.http import JsonResponse

from fight.models import Game, Fight, Step, Insult, Comeback


def begin(request):
    # TODO: fix hack.
    if Game.objects.count() == 0:
        game = Game(health=3)
        game.save()

    fight = Fight()
    fight.save()

    game = Game.objects.first()
    game.current_fight = fight
    game.save()

    # TODO: make sure steps have unique insults, if enough insults are present.
    for i in range(3):
        insult_count = Insult.objects.count()
        random_insult_index = randint(0, insult_count - 1)
        insult = Insult.objects.all()[random_insult_index]
        step = Step(index=i, insult=insult, fight=fight)
        step.save()

    first_step = Step.objects.filter(fight=fight, index=0).first()

    comebacks = [first_step.insult.correct_comeback.comeback_text]

    comeback_count = Insult.objects.count()
    for i in range(3):
        random_comeback_index = randint(0, comeback_count - 1)
        comebacks.append(Comeback.objects.all()[random_comeback_index].comeback_text)

    data = {
        'insult': first_step.insult.insult_text,
        'comebacks': comebacks
        }

    return JsonResponse(data)
