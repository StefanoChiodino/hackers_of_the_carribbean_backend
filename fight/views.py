import math
from random import randint, random, shuffle
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
    # TODO: what happens if there are less insults available than how many we take?
    all_insults: List[Insult] = [i for i in Insult.objects.all()]
    shuffle(all_insults)
    selected_insults: List[Insult] = all_insults[:3]
    for i, selected_insult in enumerate(selected_insults):
        current_step = Step(index=i, insult=selected_insult, fight=fight)
        current_step.save()

        correct_comeback = selected_insult.correct_comeback
        all_wrong_comebacks = [c for c in Comeback.objects.exclude(id=correct_comeback.id)]
        shuffle(all_wrong_comebacks)
        selected_wrong_comebacks = all_wrong_comebacks[:3]
        step_comebacks: List[Comeback] = selected_wrong_comebacks
        step_comebacks.append(correct_comeback)
        for step_comeback in step_comebacks:
            step_comeback = StepComeback(step=current_step, comeback=step_comeback)
            step_comeback.save()

    first_step = Step.objects.filter(fight=fight, index=0).first()
    step_comebacks: List[StepComeback] = StepComeback.objects.filter(step=first_step)

    data = {
        'game_id': game.id,
        'heath': game.health,
        'insult': first_step.insult.text,
        'comebacks': [sc.comeback.text for sc in step_comebacks]
        }

    return JsonResponse(data)


def step(request):
    game = get_current_game()
    if game.health is 0:
        return JsonResponse({'dead': True})

    if game.current_fight is None:
        return JsonResponse({'no_current_fight': True})

    current_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()

    fight_step_outcomes = get_fight_steps_outcomes(current_step)

    if current_step is None:
        return JsonResponse({
            'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
            'fight_finished': True
        })

    step_comebacks = StepComeback.objects.filter(step=current_step)

    data = {
        'heath': game.health,
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

    fight_step_outcomes = get_fight_steps_outcomes(current_step)

    if not successful:
        game.health = game.health - 1
        game.save()
        if game.health is 0:
            return JsonResponse({
                'game_id': game.id,
                'health': game.health,
                'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
                'dead': True
            })

    # Proceed to next step.
    game.current_fight.step_index = game.current_fight.step_index + 1
    game.current_fight.save()
    next_step = Step.objects.filter(fight=game.current_fight, index=game.current_fight.step_index).first()

    if next_step is None:
        return JsonResponse({
            'game_id': game.id,
            'health': game.health,
            'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
            'fight_finished': True
        })

    next_step_comebacks = StepComeback.objects.filter(step=next_step)

    fight_step_outcomes = get_fight_steps_outcomes(current_step)

    data = {
        'game_id': game.id,
        'health': game.health,
        'fight_steps_successful': [fso.won for fso in fight_step_outcomes],
        'insult': next_step.insult.text,
        'comebacks': [c.comeback.text for c in next_step_comebacks]
    }

    return JsonResponse(data)


def get_fight_steps_outcomes(step: Step)-> List[FightStepOutcome]:
    if step is None:
        return []
    fight_steps = Step.objects.filter(fight=step.fight)
    fight_step_outcomes: List[FightStepOutcome] = FightStepOutcome.objects.filter(step__in=fight_steps)
    return fight_step_outcomes


# http://monkeyisland.wikia.com/wiki/Insult_Sword_Fighting
insults_and_comebacks = ["You fight like a Dairy Farmer!",
                         "How appropriate! You fight like a cow!",
                         "This is the END for you, you gutter crawling cur!",
                         "And I've got a little TIP for you, get the POINT?",
                         "I've spoken with apes more polite than you!",
                         "I'm glad to hear you attended your family reunion!",
                         "Soon you'll be wearing my sword like a shish kebab!",
                         "First you better stop waving it about like a feather duster.",
                         "People fall at my feet when they see me coming!",
                         "Even BEFORE they smell your breath?",
                         "I'm not going to take your insolence sitting down!",
                         "Your hemorroids are flaring up again eh?",
                         "I once owned a dog that was smarter than you.",
                         "He must have taught you everything you know.",
                         "Nobody's ever drawn blood from me and nobody ever will.",
                         "You run THAT fast?",
                         "Have you stopped wearing diapers yet?",
                         "Why? Did you want to borrow one?",
                         "There are no words for how disgusting you are.",
                         "Yes there are. You just never learned them.",
                         "You make me want to puke.",
                         "You make me think somebody already did.",
                         "My handkerchief will wipe up your blood!",
                         "So you got that job as janitor, after all.",
                         "I got this scar on my face during a mighty struggle!",
                         "I hope now you've learned to stop picking your nose.",
                         "I've heard you are a contemptible sneak.",
                         "Too bad no one's ever heard of YOU at all.",
                         "You're no match for my brains, you poor fool.",
                         "I'd be in real trouble if you ever used them.",
                         "You have the manners of a beggar.",
                         "I wanted to make sure you'd feel comfortable with me."]


def seed(request):
    for i in range(0, math.floor(len(insults_and_comebacks) / 2)):
        comeback = Comeback(text=insults_and_comebacks[i*2 + 1])
        comeback.save()

        insult = Insult(text=insults_and_comebacks[i*2], correct_comeback=comeback)
        insult.save()


def get_current_game() -> Game:
    # TODO: fix hack.
    game = Game.objects.filter(health__gt=0).first()
    if game is not None:
        return game

    game = Game(health=3)
    game.save()
    return game
