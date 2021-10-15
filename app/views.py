from banjo.urls import route_get, route_post
from banjo.http import BadRequest
from .models import Riddle


@route_get('riddles/all')
def list_riddles(params):
    riddles = []

    for riddle in Riddle.objects.all():
        riddles.append(riddle.to_dict_answerless())

    return {'riddles':riddles}

@route_post('riddles/new')
def create_riddle(params):
    if 'question' not in params or 'answer' not in params:
        raise BadRequest("incorrect request")
    
    riddle = Riddle.from_dict(params)
    errors = riddle.validate_create()
    if len(errors) == 0:
        riddle.save()
        return {'riddle':riddle.to_dict()}
    else:
        raise BadRequest(errors[0])
        

@route_get('riddles/one')
def show_riddle(params):
    if 'id' not in params:
        raise BadRequest('incorrect request')

    id = params['id']
    riddle = Riddle.objects.get(id=id)
    return {'riddle':riddle.to_dict()}

@route_post('riddles/guess')
def guess_answer(params):
    if 'guess' not in params or 'id' not in params:
        raise BadRequest('incorrect request')

    guess = params['guess']
    id = params['id']
    riddle = Riddle.objects.get(id=id)
    
    if riddle.check_guess(guess):
        return {'correct':riddle.to_dict()}

    else:
        return {'incorrect guess':riddle.incorrect_guess()}

@route_get('riddles/difficulty')
def show_riddle(params):
    if 'id' not in params:
        raise BadRequest('incorrect request')

    id = params['id']
    riddle = Riddle.objects.get(id=id)
    return {'riddle':riddle.to_dict_difficulty()}