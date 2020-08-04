import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



#configure application
app = Flask(__name__)


'''HELPER FUNCTIONS:'''

#returns the index of the feature the computer is testing
def decision1 (features_matrix, my_board):
    probabilities = []
    for feature in features_matrix:
        probability = 0
        nelim = 0
        for i in range(len(feature)):
            if my_board[i][1] == 'True':
                nelim += 1
                probability += feature[i]

        probabilities.append(abs(probability/nelim - 0.5))

    comp_question_index = np.argmin(probabilities)
    return(comp_question_index)

#number of cards not eliminated on a board
def num_in(board):
    num_in = 0
    for card in board:
        if card[1] == 'True':
            num_in += 1
    return(num_in)

#check if someone has one card left.
def game_finished(board1, board2, correct_name):
    if correct_name == 1:
        return (True, 1)
    else:
        num_in_1 = num_in(board1)
        if num_in_1 == 1:
            return (True, 0)
        num_in_2 = num_in(board2)
        if num_in_2 == 1:
            return (True, 1)
        else:
            return (False, 2)


'''PREAMBLE'''

db = cs50.SQL("sqlite:///characters.db")

all_names = db.execute("SELECT name, id FROM characters")
list_of_features = ["hairpartition", "haircurly", "hat", "bald", "hairstuff", "hairlong", "hairginger", "hairwhite", "hairbrown", "hairblonde", "hairblack", "mouthbig", "nosebig", "cheeksred", "eyesblue", "sad", "hairfacial", "mustache", "beard", 'glasses', "earrings", "female"]
all_ = (db.execute("SELECT * FROM characters"))

features_matrix = []
for feature in list_of_features:
    feature_lst = []
    for person in all_:
        feature_lst.append(person[feature])
    #print(feature_lst)
    features_matrix.append(feature_lst)





@app.route("/play", )
def play():
    if request.method == "POST":
        #TODO #something about the sessions
        users_choice = request.form.get("choose")
        users_choice_index = np.where(user_board == users_choice) [0][0]
        #computer chooses their card
        computers_choice_index = random.randint(0, len(my_board)-1)
        computers_choice = my_board[computers_choice_index][0]

        #render the boards
        my_board = np.array([[person["name"], True] for person in all_names])
        user_board = np.array([[person["name"], True] for person in all_names])
        #redirect to the game.html page to start the questions
        return render_template("game.html", users_choice = users_choice, )
    else:
        return render_template("play.html")

