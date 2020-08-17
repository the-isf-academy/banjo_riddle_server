# This program runs the riddle server
from flask import Flask, request
from model import Riddle
from helpers import check_input

app = Flask(__name__)

@app.route('/', methods=['GET'])
def list_riddles():
    return {'riddles': [riddle.as_dict(with_answer=False) for riddle in Riddle.all()]}

@app.route('/', methods=['POST'])
def create_riddle():
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

@app.route('/<int:id>', methods=['GET'])
def show_riddle(id):
    try:
        riddle = Riddle.get(id)
        return riddle.as_dict(with_answer=False)
    except Riddle.DoesNotExist:
        return {"errors": ["riddle not found"]}, 404

@app.route('/<int:id>', methods=['POST'])
def guess_answer(id):
    try:
        riddle = Riddle.get(id)
    except Riddle.DoesNotExist:
        return {"errors": ["riddle not found"]}, 404
    data = request.get_json()
    errors = check_input(data, ["guess"])
    if len(errors) >0:
        return {"errors": errors}, 400
    correct = riddle.check_guess(data['guess'])
    riddle.save()
    return {
        "guess": data['guess'],
        "correct": correct,
        "riddle": riddle.as_dict(with_answer=correct)
    }
