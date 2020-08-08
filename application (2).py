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

#----------------------------------------------------------------------------

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
def game_fin (my_board, user_board, name_correct = False):
    #check for correct string:
    if name_correct = True:
        return ("YOU")
    else:
        if num_in(my_board) == 1:
            return ("THE COMPUTER")
        else:
            return (None)

def wipe():
    global my_board
    global user_board
    global users_choice_index
    global computers_choice_index
    global users_choice
    global computers_choice
    global is_elim
    global asked
    global winner
    is_elim = []
    asked = []

    my_board = np.array([])
    user_board = np.array([])
    users_choice = None
    computers_choice = None
    users_choice_index = None
    computers_choice_index = None

    is_elim = []
    asked = []

    winner = None

#----------------------------------------------------------------------------

'''PREAMBLE'''

db = cs50.SQL("sqlite:///characters.db")
global all_names
all_names = db.execute("SELECT name, id FROM characters")
all_names = [person["name"] for person in all_names]
list_of_features = ["hairpartition", "haircurly", "hat", "bald", "hairstuff", "hairlong", "hairginger", "hairwhite", "hairbrown", "hairblonde", "hairblack", "mouthbig", "nosebig", "cheeksred", "eyesblue", "sad", "hairfacial", "mustache", "beard", 'glasses', "earrings", "female", "male", "hairstraight", "mouthsmall", "nosesmall", "hairshort", "eyesbrown"]
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
global users_choice
global computers_choice_index
global computers_choice
global is_elim
global asked
is_elim = []
asked = []

global replies_pos
global replies_neg
global questions

global winner

replies_pos = ["have a middle part", "have curly hair", "am wearing a hat", "am bald", "am wearing hair accessories", "have long hair", "have red hair", "have white hair", "have brown hair", "have blonde hair", "have black hair",
 "have a big mouth", "have a big nose", "have red cheeks", "have blue eyes", "look sad", "have facial hair", "have a mustache", "have a beard", "am wearing glasses", "am wearing earrings", "am female", "am male", "have straight hair", "have a small mouth", "have a small nose", "have short hair", "have brown eyes"]

replies_neg = ["don't have a middle part", "don't have curly hair", "am not wearing a hat", "am not bald", "am not wearing hair accessories", "don't have long hair", "don't have red hair", "don't have white hair", "don't have brown hair", "don't have blonde hair", "don't have black hair",
 "don't have a big mouth", "don't have a big nose", "don't have red cheeks", "don't have blue eyes", "don't look sad", "don't have facial hair", "don't have a mustache", "don't have a beard", "am not wearing glasses", "am not wearing earrings", "am not female", "am not male", "don't have straight hair", "don't have a small mouth", "don't have a small nose", "don't have short hair", "don't have brown eyes"]

questions = ["Do you have a middle part", "Do you have curly hair", "Are you wearing a hat", "Are you bald", "Are you wearing hair accessories", "Do you have long hair", "Do you have red hair", "Do you have white hair", "Do you have brown hair", "Do you have blonde hair", "Do you have black hair",
 "Do you have a big mouth", "Do you have a big nose", "Do you have red cheeks", "Do you have blue eyes", "Do you look sad", "Do you have facial hair", "Do you have a mustache", "Do you have a beard", "Are you wearing glasses", "Are you wearing earrings", "Are you female", "Are you male", "Do you have straight hair", "Do you have a small mouth", "Do you have a small nose", "Do you have short hair", "Do you have brown eyes"]


#----------------------------------------------------------------------------

'''GAME IMPLEMENTATION'''

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
        global users_choice
        global is_elim
        global asked
        global computers_choice_index
        global computers_choice

        #WIPE ALL THE GAME DATA

        my_board = np.array([[person, True] for person in all_names])
        user_board = np.array([[person, True] for person in all_names])

        #users_choice = request.form.get("choose")

        for name in all_names:
            if request.form.get("choose") != None:
                users_choice = request.form.get("choose")
                break


        users_choice_index = np.where(user_board == users_choice)[0][0]

        #computer chooses their card
        computers_choice_index = random.randint(0, len(my_board)-1)
        computers_choice = my_board[computers_choice_index][0]

        my_board = my_board.tolist()
        user_board = user_board.tolist()

        # remind the user of their choice.
        flash(f" You have successfully chosen {users_choice}!")

        #redirect to the game.html page to start the questions
        return render_template("game.html", users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board, eliminated = is_elim, asked = asked)
    else:
        return render_template("choose.html")


@app.route("/game", methods=["GET", "POST"])
def game():

    '''SET UP BOARDS AND CHOICES'''
    global my_board
    global user_board
    global users_choice_index
    global users_choice
    global computers_choice_index
    global computers_choice

    global list_of_features
    global features_matrix
    global all_names

    global replies_pos
    global replies_neg
    global questions

    global asked
    global is_elim

    global winner

    users_choice = all_names[users_choice_index]

    if request.method == "POST":

        '''CHECK IF WON '''
        winner = game_fin(my_board, user_board)
        if winner != None
            return redirect ("/win")
            #return render_template("win.html", winner = winner, users_choice = users_choice, computers_choice = computers_choice)

        is_string = False

        '''USER'S TURN'''
        question_index = request.form.get('answer')
        #question_index = int(np.where(list_of_features == question_index)[0])
        try:
            question_index = int(list_of_features.index(question_index))
        except:
            question_index = request.form.get('guessname')
            is_string = True
            if question_index == computers_choice:
                winner = game_fin(my_board, user_board, True)
                return redirect ("/win")
                #return render_template("win.html", winner = winner, users_choice = users_choice, computers_choice = computers_choice)
            else:
                name_index = all_names.index(question_index)
                user_board[name_index][1] = False
                is_elim.append(question_index)

        else:
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
                    is_elim.append(user_board[i][0])
            asked.append(list_of_features[question_index])

        '''CHECK IF WON AGAIN'''
        winner = game_fin(my_board, user_board)
        if winner != None
            return redirect ("/win")
            #return render_template("win.html", winner = winner, users_choice = users_choice, computers_choice = computers_choice)

        if is_string == False:
            if has_feature == 1:
                flash(f"Computer says: Yes, I {replies_pos[question_index]}. ")
            else:
                flash(f"Computer says: No, I {replies_neg[question_index]}. ")
        else:
            flash (f"Computer says: No, I am not {question_index}. ")


        '''COMPUTERS TURN'''
        comp_question_index = decision1(features_matrix, my_board)

        if features_matrix[comp_question_index][users_choice_index] == 1:
            has_feature = 1
        else:
            has_feature = 0

        #update the comp'ss list of names
        for i in range(len(my_board)):
            if features_matrix[comp_question_index][i] != has_feature:
                #eliminate from the board
                my_board[i][1] = False


        '''CHECK IF WON AGAIN'''
        winner = game_fin(my_board, user_board)
        if winner != None
            return redirect ("/win")
            #return render_template("win.html", winner = winner, users_choice = users_choice, computers_choice = computers_choice)


        '''FLASH THE COMPUTER"S QUESTION'''
        flash(f"{questions[comp_question_index]}?")

        return render_template("game.html",  users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board, eliminated = is_elim, asked = asked)

    else:
        '''SET UP BOARDS AND CHOICES'''
        return render_template("game.html",  users_choice_index = users_choice_index, user_board = user_board, computers_choice_index = computers_choice_index, my_board = my_board, eliminated = is_elim, asked = asked)


@app.route("/win", methods=["GET"])
def win():
    #update the sql database for this session#
    global winner
    global computers_choice
    global users_choice

    if session.get("user_id") != None:
        if winner == "YOU":
            db.execute(" UPDATE users SET gamesplayed = gamesplayed + 1, gameswon = gameswon + 1 WHERE id = :user_id", user_id = session["user_id"])
        else:
            db.execute(" UPDATE users SET gamesplayed = gamesplayed + 1 WHERE id = :user_id", user_id = session["user_id"])


    #WIPE ALL THE GAME DATA
    temp_computer_choice = computers_choice
    temp_user_choice = users_choice
    temp_winner = winner

    global is_elim
    is_elim.clear()
    global asked
    asked.clear()

    wipe()

    return render_template("win.html", winner = temp_winner, users_choice = temp_user_choice, computers_choice = temp_computer_choice)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("please provide a valid username")
            return render_template("register.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide a valid password")
            return render_template("register.html")
        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            flash("Passwords must match")
            return render_template("register.html")

        username = request.form.get('username')
        password = request.form.get('password')


        # insert username + hashed pw into the database
        hashed = generate_password_hash(password)

        names = db.execute("SELECT username FROM users where username = :username",
                                 username=username)


        new_user = db.execute("INSERT INTO users (username, gamesplayed, gameswon, hash) VALUES(:username, 0, 0, :hashed)",
                                 username=username,
                                 hashed=hashed)

        # Ensure username doesnt already exist:
        if not new_user:
            flash("Username already taken")
            return render_template("register.html")

        # Remember which user has logged in
        session["user_id"] = new_user

        # Display a flash message
        flash("Registration Successful!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Error 403, Enter valid Username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Error 403, Enter valid Password")
            return redirect("/login")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) < 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Error 403, Enter valid Username and Password")
            return redirect("/login")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/account")
def account():
    #TODO
    userinfo = db.execute("SELECT * FROM users WHERE id = :user_id",
                      user_id=session["user_id"])[0]

    return render_template("account.html", user = userinfo)

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    users = db.execute("SELECT * FROM users ORDER BY gameswon DESC")
    return render_template("leaderboard.html", users = users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


