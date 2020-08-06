import os
import cs50
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import numpy as np
import random


#configure application
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12).hex()

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
global all_names
all_names = db.execute("SELECT name, id FROM characters")
all_names = [person["name"] for person in all_names]
list_of_features = ["hairpartition", "haircurly", "hat", "bald", "hairstuff", "hairlong", "hairginger", "hairwhite", "hairbrown", "hairblonde", "hairblack", "mouthbig", "nosebig", "cheeksred", "eyesblue", "sad", "hairfacial", "mustache", "beard", 'glasses', "earrings", "female", "male", "hairstraight", "mouthsmall", "nosesmall", "hairshort"]
all_ = (db.execute("SELECT * FROM characters"))

global features_matrix
features_matrix = []
for feature in list_of_features:
    feature_lst = []
    for person in all_:
        feature_lst.append(person[feature])
    #print(feature_lst)
    features_matrix.append(feature_lst)

global my_board
global user_board
global users_choice_index
global computers_choice_index
global computers_choice
global is_elim
is_elim = set()


@app.route("/", methods=["GET"])
def about():
    return render_template("about.html")



@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "POST":
        #TODO #something about the sessions
        global all_names
        #render the boards
        global my_board
        global user_board
        global users_choice_index

        global computers_choice_index
        global computers_choice
        my_board = np.array([[person, True] for person in all_names])
        user_board = np.array([[person, True] for person in all_names])

        #users_choice = request.form.get("choose")

        for name in all_names:
            if request.form.get("choose") != None:
                users_choice = request.form.get("choose")
                break


        users_choice_index = np.where(user_board == users_choice)[0][0]
        flash(f"Users choice index = {users_choice_index}")

        #computer chooses their card
        computers_choice_index = random.randint(0, len(my_board)-1)
        computers_choice = my_board[computers_choice_index][0]

        my_board = my_board.tolist()
        user_board = user_board.tolist()

        # remind the user of their choice.
        flash(f" you have successfully chosen {users_choice}")

        #redirect to the game.html page to start the questions
        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)
    else:
        return render_template("choose.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #TODO


        return render_template("register.html")
    else:
        return render_template("register.html")







@app.route("/game", methods=["GET", "POST"])
def game():
    global my_board
    global user_board
    global users_choice_index
    global computers_choice_index
    global computers_choice

    global list_of_features
    global features_matrix

    if request.method == "POST":


        '''SET UP BOARDS AND CHOICES'''


        '''CHECK IF WON'''
        if num_in(user_board) == 1 or num_in(my_board) == 1:
            winner = game_finished(my_board, user_board, 0)
            '''GO TO WINNING PAGE'''
            flash(f"THE WINNER IS {winner}")
            return render_template("choose.html")

        '''USER'S TURN'''
        question_index = request.form.get('answer')
        #question_index = int(np.where(list_of_features == question_index)[0])
        question_index = int(list_of_features.index(question_index))


        #ADD A SECTION FOR IF THE USER INPUTS A NAME
        #Ask the question
        if features_matrix[question_index][computers_choice_index] == 1:
            has_feature = 1
            flash(f"Yes, I have{list_of_features[question_index]}")
        else:
            has_feature = 0
            flash(f"No, I dont have{list_of_features[question_index]}")

        #Update the user's board
        for i in range(len(user_board)):
            if features_matrix[question_index][i] != has_feature:
                #eliminate from the board
                user_board[i][1] = False

        '''CHECK IF WON AGAIN'''
        if num_in(user_board) == 1 or num_in(my_board) == 1:
            winner = game_finished(my_board, user_board, 0)
            '''GO TO WINNING PAGE'''
            flash(f"THE WINNER IS {winner}")
            return render_template("choose.html")


        '''COMPUTERS TURN'''
        comp_question_index = decision1(features_matrix, my_board)

        if features_matrix[comp_question_index][users_choice_index] == 1:
            has_feature = 1

            #print answer
            #print(f"yes, your person has {list_of_features[comp_question_index]}")
        else:
            has_feature = 0
            #print(f"no, your person doesnt have {list_of_features[comp_question_index]}")

        #update the user's list of names
        for i in range(len(my_board)):
            if features_matrix[comp_question_index][i] != has_feature:
                #eliminate from the board
                my_board[i][1] = False
                is_elim.add(my_board[i][0])

        '''FLASH SOMETHING FOR THE RESULT OF THE USERS QUESTION'''


        '''FLASH THE COMPUTER"S QUESTION'''
        flash(f"Does your person have{list_of_features[comp_question_index]}")

        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)

    else:
        '''SET UP BOARDS AND CHOICES'''

        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)




