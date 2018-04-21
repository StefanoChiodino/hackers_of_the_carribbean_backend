from random import randint, random

from django.http import JsonResponse

from fight.models import Game, Fight, Step, Insult, Comeback, StepComeback


def begin(request):
    # Create new fight.
    fight = Fight()
    fight.save()

    # Set the new fight as the current fight.
    game = get_current_game()
    game.current_fight = fight
    game.save()

    # Create steps with random insults and the possible comebacks.
    # TODO: make sure steps have unique insults, if enough insults are present.
    for i in range(3):
        # Create step with random insult.
        insult_count = Insult.objects.count()
        random_insult_index = randint(0, insult_count - 1)
        insult = Insult.objects.all()[random_insult_index]
        current_step = Step(index=i, insult=insult, fight=fight)
        current_step.save()

        # Generate possible comebacks for the step.
        comebacks = [current_step.insult.correct_comeback.text]
        comeback_count = Insult.objects.count()
        for _ in range(3):
            random_comeback_index = randint(0, comeback_count - 1)
            random_comeback = Comeback.objects.all()[random_comeback_index]
            comebacks.append(random_comeback.text)

            # Save comebacks.
            step_comeback = StepComeback(step=current_step, comeback=random_comeback)
            step_comeback.save()

    first_step = Step.objects.filter(fight=fight, index=0).first()
    step_comebacks = StepComeback.objects.filter(step=first_step)

    data = {
        'insult': first_step.insult.text,
        'comebacks': [sc.comeback.text for sc in step_comebacks]
        }

    return JsonResponse(data)


def step(request):
    game = get_current_game()
    current_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()
    step_comebacks = StepComeback.objects.filter(step=current_step)

    data = {
        'insult': current_step.insult.text,
        'comebacks': [c.comeback.text for c in step_comebacks]
    }

    return JsonResponse(data)


def get_current_game() -> Game:
    # TODO: fix hack.
    if Game.objects.count() == 0:
        game = Game(health=3)
        game.save()
    return Game.objects.filter(health__gt=0).first()
