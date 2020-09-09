# This program runs the riddle server
from flask import Flask, request
from model import Riddle

app = Flask(__name__)

@app.route('/riddles/all', methods=['GET'])
def list_riddles():
    "Returns a list of all the riddles, without answers, and in order of difficulty."
    return {'riddles': [riddle.as_dict(with_answer=False) for riddle in Riddle.all()]}

@app.route('/riddles/new', methods=['POST'])
def create_riddle():
    "Creates a new riddle and returns it. Requires `question` and `answer` params."
    data = request.get_json()
    errors = check_input(data, ["question", "answer"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    riddle = Riddle(**data)
    errors = riddle.validate()
    if len(errors) >0:
        return {"errors": errors}, 400
    riddle.save()
    return riddle.as_dict(with_answer=True)

@app.route('/riddles/one', methods=['GET'])
def show_riddle():
    "Returns one riddle, without its answer."
    data = request.get_json()
    errors = check_input(data, ["id"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    try:
        riddle = Riddle.get(data['id'])
        return riddle.as_dict(with_answer=False)
    except Riddle.DoesNotExist:
        return {"errors": ["riddle not found"]}, 404

@app.route('/riddles/guess', methods=['POST'])
def guess_answer():
    "Accepts a `guess` param and returns whether or not it was correct."
    data = request.get_json()
    errors = check_input(data, ["id", "guess"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    try:
        riddle = Riddle.get(data['id'])
    except Riddle.DoesNotExist:
        return {"errors": ["riddle not found"]}, 404
    correct = riddle.check_guess(data['guess'])
    riddle.save()
    return {
        "guess": data['guess'],
        "correct": correct,
        "riddle": riddle.as_dict(with_answer=correct)
    }

def check_input(values_dict, expected):
    """
    A helper to ensure that the data sent with a POST request
    contains all expected params and no unexpected params. 
    """
    errors = []
    if values_dict is None:
        return ["no data provided"]
    for key in values_dict.keys():
        if key not in expected:
            errors.append("unexpected field: {}".format(key))
    for key in expected:
        if key not in values_dict.keys():
            errors.append("missing field: {}".format(key))
    return errors
