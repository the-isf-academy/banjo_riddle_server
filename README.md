# Riddle server

Riddle server is a simple HTTP server for learning about how computers
communicate over the Internet. 

## Usage

If you already know the IP address and port of a running Riddle server, you can
interact with it using HTTP requests. In these examples, we will use the
`HTTPie` library to send HTTP requests from Terminal.

We are connecting to `127.0.0.1:5000`, which is the address of the Riddle server
when it is running locally.

## List the riddles
```
$ http GET 127.0.0.1:5000 

{
    "riddles": [
        {
            "correct": 0,
            "guesses": 0,
            "id": 1,
            "question": "What is orange and sounds like a parrot?"
        }
    ]
}
```

## Add a riddle

```
$ http POST 127.0.0.1:5000 question="What is black and white and red all over?" answer="A newspaper"

{
    "answer": "A newspaper",
    "correct": 0,
    "guesses": 0,
    "id": 2,
    "question": "What is black and white and red all over?"
}
```

## Guess the answer to a riddle

```
$ http POST 127.0.0.1:5000/2 guess="Carrot"

{
    "correct": true,
    "guess": "Carrot",
    "riddle": {
        "answer": "A carrot",
        "correct": 1,
        "guesses": 1,
        "id": 2,
        "question": "What is orange and sounds like a parrot?"
    }
}
```


## Installation

First, you may want to create a virtual environment:

```
$ python3 -m venv env 
# source env/bin/activate
```

Now install the Riddle server.

```
$ git clone https://github.com/cproctor/riddle_server.git
$ cd riddle_server
$ pip install -r requirements.txt
```

Finally, run the server.

```
$ ./run.sh
```
