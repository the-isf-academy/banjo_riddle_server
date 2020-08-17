import sqlite3
from pathlib import Path
from fuzzywuzzy import fuzz

DATABASE = "riddles.db"
SCHEMA = """
CREATE TABLE riddles (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL, 
    answer TEXT NOT NULL, 
    guesses INTEGER NOT NULL, 
    correct INTEGER NOT NULL
)
"""

class Riddle:
    """This is the Riddle model. 

    A Riddle represents a riddle, with a question, an answer, and a couple of 
    numbers keeping track of how many times the riddle has been guessed and 
    how many times it has been guessed correctly.
    """
    MIN_FUZZ_RATIO = 80

    class DoesNotExist(Exception):
        "This is a custom error we'll use when a riddle is requested which does not exist."

    @classmethod
    def all(cls):
        "Returns all riddles, sorted by difficulty"
        connection, cursor = cls.connect()
        query = "SELECT id, question, answer, guesses, correct FROM RIDDLES"
        cursor.execute(query)
        result = [Riddle(*values) for values in cursor.fetchall()]
        connection.close()
        riddles = sorted(result, key=lambda r: r.difficulty())
        return riddles

    def __init__(self, id=None, question=None, answer=None, guesses=0, correct=0):
        self.id = id
        self.question = question
        self.answer = answer
        self.guesses = guesses
        self.correct = correct

    def __repr__(self):                                                                                                                                         
        """Declares how to represent a Riddle as a string.                                                                                                     

        A riddle's string will look something like this:                                                                                                       
        <Riddle 12: Where can you get dragon milk? (3/15)>
        """
        return "<Riddle {}: {} ({}/{})>".format(self.id or '(unsaved)', self.question, self.correct, self.guesses)                                                   
    def save(self):
        connection, cursor = self.connect()
        if self.id:
            query = "UPDATE riddles SET question=?, answer=?, guesses=?, correct=? WHERE id = ?"
            cursor.execute(query, self.values() + [self.id])
        else:
            query = "INSERT INTO riddles (question,answer,guesses,correct) VALUES (?,?,?,?)"
            cursor.execute(query, self.values())
            cursor.execute("SELECT last_insert_rowid()")
            values = cursor.fetchone()
            self.id = values[0]
        connection.commit()
        connection.close()

    def is_valid(self):
        "Checks whether this riddle is valid. In other words, when validate() finds no errors."
        return len(self.validate()) == 0

    def validate(self):
        "Checks whether this riddle can be saved"
        errors = []
        if self.question is None:
            errors.append("question is required")
        if self.answer is None:
            errors.append("question is required")
        return errors

    def difficulty(self):
        return (self.correct + 1) / (self.guesses + 1)

    def as_dict(self, with_answer=True):
        properties = ["id", "question", "answer", "guesses", "correct"]
        return {prop: value for prop, value in zip(properties, self.values(with_id=True)) if with_answer or prop != 'answer'}

    def values(self, with_id=False):
        "Returns values ready to pass to the database"
        values = [self.question, self.answer, self.guesses, self.correct]
        if with_id:
            return [self.id] + values
        else:
            return values
                                                                                                                                                               
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
        - "idk"             40                                                                                                                                 
        """
        self.guesses += 1                                                                                                                                     
        similarity = fuzz.ratio(guess.lower(), self.answer.lower())                                                                                            
        if similarity >= self.MIN_FUZZ_RATIO:                                                                                                                  
            self.correct+= 1                                                                                                                          
            return True
        else:
            return False  

    @classmethod
    def get(self, id):
        connection, cursor = self.connect()
        query = "SELECT * FROM riddles WHERE id=?" 
        cursor.execute(query, [id])
        values = cursor.fetchone()
        if values is None:
            raise Riddle.DoesNotExist()
        return Riddle(*values)

    @classmethod
    def connect(cls):
        "Connects to the database and returns a cursor"
        cls.check_for_db()
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        return connection, cursor

    @classmethod
    def check_for_db(cls):
        "If the database does not exist, set it up."
        if not Path(DATABASE).exists():
            connection = sqlite3.connect(DATABASE)
            connection.execute(SCHEMA)
            connection.close()
    
