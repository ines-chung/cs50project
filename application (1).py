import os
import cs50
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

global features_matrix
features_matrix = []
for feature in list_of_features:
    feature_lst = []
    for person in all_:
        feature_lst.append(person[feature])
    #print(feature_lst)
    features_matrix.append(feature_lst)



@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")

@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "POST":
        #TODO #something about the sessions

        #render the boards
        my_board = np.array([[person["name"], True] for person in all_names])
        user_board = np.array([[person["name"], True] for person in all_names])

        users_choice = request.form.get("choose")
        users_choice_index = np.where(user_board == users_choice) [0][0]

        #computer chooses their card
        computers_choice_index = random.randint(0, len(my_board)-1)
        computers_choice = my_board[computers_choice_index][0]



        #redirect to the game.html page to start the questions
        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)
    else:
        return render_template("choose.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        '''
        if coming from play.html

        else:
            BLAH

        '''

        '''SET UP BOARDS AND CHOICES'''
        my_board = request.args.get('my_board')
        user_board = request.args.get('user_board')

        users_choice_index =  request.args.get('users_choice_index')

        computers_choice_index = request.args.get('computers_choice_index')
        computers_choice = my_board[computers_choice_index][0]

        global list_of_features
        global features_matrix

        '''CHECK IF WON'''
        if num_in(user_board) == 1 or num_in(my_board) == 1:
            winner = game_finished(my_board, user_board, 0)
            '''GO TO WINNING PAGE'''
            flash(f"THE WINNER IS {winner}")
            return render_template("play.html")

        '''USER'S TURN'''
        question_index = request.form.get('answer')
        question_index = int(np.where(list_of_features == question_index)[0])

        #ADD A SECTION FOR IF THE USER INPUTS A NAME
        #Ask the question
        if features_matrix[question_index][computers_choice_index] == 1:
            has_feature = 1
        else:
            has_feature = 0

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
        comp_question_index = decision1(comp_features_matrix, my_board)

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

        '''FLASH SOMETHING FOR THE RESULT OF THE USERS QUESTION'''
        flash(f"No, I dont have{list_of_features[question_index]}")

        '''FLASH THE COMPUTER"S QUESTION'''
        flash(f"Does your person have{list_of_features[comp_question_index]}")


        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)

    else:
        '''SET UP BOARDS AND CHOICES'''
        my_board = request.args.get('my_board')
        user_board = request.args.get('user_board')

        users_choice_index =  request.args.get('users_choice_index')

        computers_choice_index = request.args.get('computers_choice_index')
        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board)
