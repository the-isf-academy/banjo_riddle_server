from banjo.urls import route_get, route_post
from banjo.http import BadRequest
from .models import Riddle

@route_get('riddles/all')
def list_riddles(params):
    riddles = []
    for riddle in Riddle.objects.all():
        riddles.append(riddle.to_dict_answerless())
    return {'riddles':riddles}

@route_post('riddles/new', args={'question': str, 'answer': str})
def create_riddle(params):
    riddle = Riddle.from_dict(params)
    errors = riddle.validate_create()
    if len(errors) == 0:
        riddle.save()
        return {'riddle':riddle.to_dict()}
    else:
        raise BadRequest(errors[0])

@route_get('riddles/one', args={'id': int})
def show_riddle(params):
    riddle = Riddle.objects.get(id=params['id'])
    return {'riddle':riddle.to_dict()}

@route_post('riddles/guess', args={'id': int, 'guess': str})
def guess_answer(params):
    riddle = Riddle.objects.get(id=params['id'])
    if riddle.check_guess(params['guess']):
        return {'correct':riddle.to_dict()}
    else:
        return {'incorrect guess':riddle.incorrect_guess()}

@route_get('riddles/difficulty', args={'id': int})
def get_riddle_difficuly(params):
    riddle = Riddle.objects.get(id=params['id'])
    return {'riddle':riddle.to_dict_difficulty()}
