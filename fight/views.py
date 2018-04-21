from random import randint, random

from fight.models import Game, Fight, Step, Insult


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
        random_insult_index = random.randint(0, insult_count - 1)
        insult = Insult.objects.all()[random_insult_index]
        step = Step(index=i, insult=insult, fight=fight)
        step.save()

    first_step = Step.objects.filter(fight=fight, index=0)

    return first_step
