from banjo.urls import route_get, route_post
from banjo.http import BadRequest
from app.models import Riddle

@route_get('riddles/all')
def list_riddles(params):
    riddles = sorted(Riddle.objects.all(), key=lambda riddle: riddle.difficulty())
    return {'riddles': riddle.to_dict(with_answer=False) for riddle in riddles}

@route_post('riddles/new')
def create_riddle(params):
    riddle = Riddle.from_dict(params)
    errors = riddle.validate()
    if len(errors) == 0:
        riddle.save()
        return riddle.as_dict(with_answer=False)
    else:
        raise BadRequest()
        

#@app.route('/riddles/one', methods=['GET'])
#def show_riddle():

#@app.route('/riddles/guess', methods=['POST'])
#def guess_answer():
