from banjo.urls import route_get, route_post
from banjo.http import BadRequest
from .models import Riddle

@route_get('all')
def list_riddles(params):
    riddles = []

    if len(Riddle.objects.all())  > 0:

        for riddle in Riddle.objects.all():
            riddles.append(riddle.to_dict_answerless())

        return {'riddles':riddles}
    
    else:
        return {'error': 'no riddles exist'}


@route_post('riddle/new', args={'question': str, 'answer': str})
def create_riddle(params):
    riddle = Riddle.from_dict(params)
    errors = riddle.validate_create()
    
    if len(errors) == 0:
        riddle.save()
        return {'riddle':riddle.to_dict()}



@route_get('riddle/one', args={'id': int})
def one_riddle(args):

    id = args['id']

    if Riddle.objects.filter(id=id).exists():
        riddle = Riddle.objects.get(id=id)
        return {'riddle':riddle.to_dict()}

    else:
        return {'error': 'riddle does not exist'}

@route_post('riddle/guess', args={'id': int, 'guess': str})
def guess_answer(params):
    guess = params['guess']
    id = params['id']
    
    if Riddle.objects.filter(id=id).exists():
        riddle = Riddle.objects.get(id=id)
        if riddle.check_guess(guess):
            # riddle_dict = riddle.to_dict()
            return {'riddle':riddle.correct_guess()}

        else:
            return {'riddle':riddle.incorrect_guess()}
        
    else:
        return {'error': 'riddle does not exist'}

    

@route_get('riddle/difficulty', args={'id': int})
def get_riddle_difficuly(params):
    riddle = Riddle.objects.get(id=params['id'])

    id = params['id']

    if Riddle.objects.filter(id=id).exists():
        riddle = Riddle.objects.get(id=id)
        return {'riddle':riddle.to_dict_difficulty()}
        
    else:
        return {'error': 'riddle does not exist'}

