from banjo.urls import route_get, route_post
from banjo.http import BadRequest
from .models import Riddle

@route_get('riddles/all')
def list_riddles(params):
    riddles = []
    print(Riddle.objects.all())
    for riddle in Riddle.objects.all():
        print('hi')
        print(riddle.to_dict())
        riddles.append(riddle.to_dict())
    return {'riddles':riddles}

@route_post('riddles/new')
def create_riddle(params):
    riddle = Riddle.from_dict(params)
    errors = riddle.validate_create()

    if len(errors) == 0:
        riddle.save()
        return {'riddle',riddle.to_dict()}
    else:
        raise BadRequest(errors[0])
        

@route_get('riddles/one')
def show_riddle(params):
    id = params['id']
    riddle = Riddle.objects.filter(id=id)[0]
    return {'riddle':riddle.to_dict()}

@route_post('riddles/guess')
def guess_answer(params):
    guess = params['guess']
    id = params['id']
    riddle = Riddle.objects.filter(id=id)[0]
    
    if riddle.check_guess(guess):
        return {'correct':riddle.to_dict()}

    else:
        return {'incorrect guess':riddle.incorrect_guess()}