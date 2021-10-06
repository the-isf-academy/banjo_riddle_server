# RiddleView
# ------------------
# By Chris Proctor
# RiddleView provides a nice user interface for guessing riddles. 

from api import RiddleAPI

class RiddleView:
    "Allows a player to interact with a Riddle Server from the Terminal"
    def __init__(self, url):
        self.api = RiddleAPI(url)

    def run(self):
        print("Welcome to the Riddler")
        print("Press control + c to quit")
        print("-" * 80)
        self.show_menu()

    def show_menu(self):
        choices = [
            "Show riddles",
            "Random riddle", 
            "Add a riddle"
        ]
        choice = self.get_choice("What do you want to do?", choices)
        
        if choice == 0:
            self.list_riddles()
        elif choice == 1:
            riddle = self.api.get_random_riddle()
            self.ask_riddle(riddle['id'])
        elif choice == 2:
            self.add_riddle()

    def list_riddles(self):
        riddles = self.api.get_all_riddles()
        if len(riddles) == 0:
            print("Sorry, there are no riddles on the server!")
            self.show_menu()
        else:
            choices = [riddle['question'] for riddle in riddles]
            choice = self.get_choice("Which riddle do you want to guess?", choices)
            riddle_id = riddles[choice]['id']
            self.ask_riddle(riddle_id)

    def ask_riddle(self, riddle_id):
        riddle = self.api.get_riddle(riddle_id)
        print(riddle['question'])
        guess = input("> ")
        correct = self.api.guess_riddle(riddle_id, guess)
        if correct:
            print("Yes!")
        else:
            print("Nope, that's not the answer.")
        self.show_menu()

    def add_riddle(self):
        question = input("question: ")
        answer = input("answer: ")
        choices = ["Add it!", "Edit", "Never mind"]
        choice = self.get_choice(question + " " + answer, choices)
        if choice == 0:
            self.api.add_riddle(question, answer)
            self.show_menu()
        elif choice == 1:
            self.add_riddle()
        elif choice == 2:
            self.show_menu()

    def get_choice(self, prompt, choices):
        print(prompt)
        for i, choice in enumerate(choices):
            print("{}. {}".format(i, choice))
        while True:
            selection = input("> ")
            if selection.isdigit():
                number = int(selection)
                if number >= 0 and number < len(choices):
                    return number
            print("Please try again")

if __name__ == '__main__':
    # Here we're adding an argument, so the user can optionally provide a different 
    # riddle server URL. ArgumentParser handles this option and also provides a nice help
    # message. Try it out by running `python view.py --help`.
    from argparse import ArgumentParser
    parser = ArgumentParser("Riddle Client")
    parser.add_argument("--server", default="http://138.68.28.249:5000", help="The URL of the Riddle Server")
    args = parser.parse_args()
    view = RiddleView(args.server)
    view.run()
