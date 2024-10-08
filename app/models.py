from banjo.models import Model, StringField, IntegerField
# from fuzzywuzzy import fuzz

class Riddle(Model):
    question = StringField()
    answer = StringField()
    guesses = IntegerField()
    correct = IntegerField()

    MIN_FUZZ_RATIO = 80
    
    def __repr__(self):
        """Declares how to represent a Riddle as a string
        A riddle's string will look something like this
        <Riddle 12: Where can you get dragon milk? (3/15)>
        """
        return "<Riddle {}: {} ({}/{})>".format(
            self.id or '(unsaved)', 
            self.question, 
            self.correct, 
            self.guesses
        )
    


    def to_dict_answerless(self):
        return {
            "correct": self.correct,
            "guesses": self.guesses,
            "id": self.id,
            "question": self.question
        }

    def to_dict_difficulty(self):
        return {
            "id": self.id,
            "question": self.question,
            "difficulty": self.difficulty(),
        }

    def is_valid(self):
        "Checks whether this riddle is valid. In other words, when validate() finds no errors."
        return len(self.validate()) == 0

    def validate_create(self):
        "Checks whether this riddle can be saved"
        errors = []
        if self.question == "":
            errors.append("question is required")
        if self.answer == "":
            errors.append("answer is required")
        return errors

    def difficulty(self):
        """Calculates and returns the riddle's difficulty. 

        The difficulty is basically 1 minus the fraction of guesses which were correct. 
        So a Riddle with a difficulty of 1 is impossibly hard, while a Riddle with a difficulty 
        of 0 is easy--everyone gets it right!

        There is an interesting detail here though. Instead of 1 - correct/guesses, we add 1 to 
        correct and we add 1 to guesses. This is called "smoothing" and it provides two benefits:
        First, we avoid having an undefined difficulty when there have been no guesses (0/0 would 
        raise a ZeroDivisionError) Second, it gives better values for difficulty when there have been no 
        correct guesses or no incorrect guesses. Consider an impossible riddle:

        Number of wrong guesses     Difficulty with smoothing   Difficulty without smoothing
        0                           0                           error
        1                           0.5                         1
        2                           0.66                        1
        3                           0.75                        1
        4                           0.8                         1
        100                         0.99                        1
        1000                        0.999                       1

        With smoothing, a Riddle's difficulty can only be really high if there are few correct guesses
        and a lot of guesses. This seems like the right way to define difficulty.
        """
        return 1 - (self.correct + 1) / (self.guesses + 1)


    def check_guess(self, guess):
        """Checks whether a guess is correct and logs the attempt.
        We don't want to be too strict, so we will accept guesses which are close to the answer.
        Fuzzy string-matching is an interesting problem, which we will sidestep by using the
        `fuzzywuzzy` library. `FUZZ_RATIO` is our limit for how similar the answers have to be.
        Also, we don't care about upper-case and lower-case, so we'll cast everything to lower.
        For example, consider the riddle, "What's brown and sticky?" The answer, of course, is
        "A stick" Here are some attempts with their fuzz ratios:                                                                                               
        - "a stick"         100
        - "a stik"          92
        - "stick"           83
        - "it's a stick"    74
        - "idk"             40                                                                                             """
        self.guesses += 1
        # similarity = fuzz.ratio(guess.lower(), self.answer.lower())
        
        if guess == self.answer:
            self.correct+= 1
            self.save()
            return True
        else:
            self.save()
            return False
        

    def correct_guess(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "correct": self.correct,
            "guesses": self.guesses,
            'correct': True
        }

    def incorrect_guess(self):
        return(
            {'id': self.id,
            'question': self.question,
            'guesses': self.guesses,
            'correct': False}
        )
