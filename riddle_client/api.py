# RiddleAPI
# ---------
# By Chris Proctor
# The Riddle API takes care of connecting to the server. 

import requests
from random import choice

class APIError(Exception):
    "A custom error we'll use when something goes wrong with the API"

class RiddleAPI:
    "Provides an easy way for Python programs to interact with a Riddle Server"
    def __init__(self, server):
        self.server = server

    def get_all_riddles(self):
        "Fetches all the riddles from the server"
        route = "/riddles/all"
        response = requests.get(self.server + route)
        if response.ok:
            return response.json()['riddles']
        else:
            raise APIError(response.json()['errors'])
            
    def guess_riddle(self, riddle_id, guess):
        "Submits a guess to the server. Returns True or False"
        route = "/riddles/guess"
        payload = {'id': riddle_id, 'guess': guess}
        response = requests.post(self.server + route, json=payload)
        if response.ok:
            return response.json()
        else:
            raise APIError(response.json()['errors'])

    def get_riddle(self, riddle_id):
        "Fetches a single riddle from the server"
        route = "/riddles/one"
        raise APIError("The API doesn't support `get_riddle` yet. Can you add it?")

    def get_random_riddle(self):
        "Fetches all riddles from the server and then randomly returns one"
        raise APIError("The API doesn't support `get_random_riddle` yet. Can you add it?")

    def add_riddle(self, question, answer):
        "Adds a new riddle to the server"
        route = "/riddles/new"
        raise APIError("The API doesn't support `add_riddle` yet. Can you add it?")


    

