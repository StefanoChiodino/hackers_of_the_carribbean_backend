from random import randint, random
from typing import List

from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fuzzywuzzy import fuzz

from fight.models import Game, Fight, Step, Insult, Comeback, StepComeback, FightStepOutcome


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

        # Save correct comebacks.
        # TODO: randomise comebacks.
        step_comeback = StepComeback(step=current_step, comeback=insult.correct_comeback)
        step_comeback.save()

        # Generate other possible comebacks for the step.
        comebacks = [current_step.insult.correct_comeback.text]
        comeback_count = Insult.objects.count()
        for _ in range(3):
            random_comeback_index = randint(0, comeback_count - 1)
            random_comeback = Comeback.objects.all()[random_comeback_index]
            comebacks.append(random_comeback.text)

            # Save incorrect comeback.
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
    if game.health is 0:
        return JsonResponse({'dead': True})

    current_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()

    if current_step is None:
        return JsonResponse({'fight_finished': True})

    step_comebacks = StepComeback.objects.filter(step=current_step)

    fight_steps = Step.objects.filter(fight=current_step.fight)
    fight_step_outcomes: QuerySet[FightStepOutcome] = FightStepOutcome.objects.filter(step__in=fight_steps)

    data = {
        'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
        'insult': current_step.insult.text,
        'comebacks': [c.comeback.text for c in step_comebacks]
    }

    return JsonResponse(data)


@csrf_exempt
def comeback(request):
    comeback_text = request.body.decode('utf-8')
    game = get_current_game()
    current_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()
    step_comebacks = StepComeback.objects.filter(step=current_step)
    correct_comeback = current_step.insult.correct_comeback

    # Find most probable comeback.
    step_comebacks_by_match_score: List[StepComeback] =\
        sorted(step_comebacks, key=lambda sc: fuzz.ratio(comeback_text, sc.comeback.text))
    step_comebacks_by_match_score.reverse()
    matched_comeback = step_comebacks_by_match_score[0]

    # Save outcome.
    successful = matched_comeback.comeback.id is correct_comeback.id
    fight_step_outcome: FightStepOutcome = FightStepOutcome(step=current_step, won=successful)
    fight_step_outcome.save()

    if successful:
        game.health = game.health - 1
        if game.health is 0:
            return JsonResponse({'dead': True})

    # Proceed to next step.
    game.current_fight.step_index = game.current_fight.step_index + 1
    game.current_fight.save()
    next_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()
    if next_step is None:
        return JsonResponse({'fight_finished': True})

    next_step_comebacks = StepComeback.objects.filter(step=next_step)

    fight_steps = Step.objects.filter(fight=current_step.fight)
    fight_step_outcomes: QuerySet[FightStepOutcome] = FightStepOutcome.objects.filter(step__in=fight_steps)

    data = {
        'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
        'insult': next_step.insult.text,
        'comebacks': [c.comeback.text for c in next_step_comebacks]
    }

    return JsonResponse(data)


def get_current_game() -> Game:
    # TODO: fix hack.
    game = Game.objects.filter(health__gt=0).first()
    if game is not None:
        return game

    game = Game(health=3)
    game.save()
    return game
