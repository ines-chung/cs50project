from math import *
import cs50
import numpy as np
import random


'''PREAMBLE'''

db = cs50.SQL("sqlite:///characters.db")

all_names = db.execute("SELECT name, id FROM characters")

my_board = np.array([[person["name"], True] for person in all_names])
user_board = np.array([[person["name"], True] for person in all_names])


list_of_features = ["hairpartition", "haircurly", "hat", "bald", "hairstuff", "hairlong", "hairginger", "hairwhite", "hairbrown", "hairblonde", "hairblack", "mouthbig", "nosebig", "cheeksred", "eyesblue", "sad", "hairfacial", "mustache", "beard", 'glasses', "earrings", "female"]
all_ = (db.execute("SELECT * FROM characters"))


features_matrix = []
for feature in list_of_features:
    feature_lst = []
    for person in all_:
        feature_lst.append(person[feature])
    #print(feature_lst)
    features_matrix.append(feature_lst)

user_features_matrix = np.array(features_matrix)
comp_features_matrix = np.array(features_matrix)

user_asked = set()

'''CHOOSING CARDS'''
#computer chooses their card
computers_choice_index = random.randint(0, len(my_board)-1)
computers_choice = my_board[computers_choice_index][0]
print ("computer chose:", computers_choice)

#User choose their card
users_choice = input("Choose a card: ")
users_choice_index = np.where(user_board == users_choice) [0][0]
#users_choice_features = db.execute("SELECT mouth, nose, cheeks_rosy, eyes, hair_color, hair_length, hair_texture, hair_midpart, glasses, earrings, hat, wrinkles, hair_facial  FROM characters WHERE name LIKE :name", name = users_choice)
print(users_choice_index)

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
def game_finished(my_board, user_board, correct_name):
    if correct_name == 1:
        return ('User')
    else:
        num_in_1 = num_in(my_board)
        if num_in_1 == 1:
            return ('Computer')
        num_in_2 = num_in(user_board)
        if num_in_2 == 1:
            return ("User")
        else:
            return ("None")


'''GAME'''

while (True):
    
    '''CHECK IF WON'''
    if num_in(user_board) == 1 or num_in(my_board) == 1:
        winner = game_finished(my_board, user_board, 0)
        break
    
    '''USER'S TURN'''
    #index of the feature the user wants to question:
    question_index = input("What feature are you gonna ask about?")
    try:
        question_index = int(question_index)
        
    #If the user entered a string, check to see if it is the computer's choice name. 
    except:
        if question_index == computers_choice:
            game = game_finished(my_board, user_board, 1)
            break
        else:
            user_board[np.where(user_board == question_index)[0]][1] = False
    else: 
        #dont ask the same question twice
        user_asked.add(question_index)
        #Ask the question
        if features_matrix[question_index][computers_choice_index] == 1:
            has_feature = 1  
            #print answer
            print(f"yes, my person is {list_of_features[question_index]}")
        else:
            has_feature = 0
            print(f"no, my person isnt {list_of_features[question_index]}")
        
        #Update the user's board
        for i in range(len(user_board)):
            if user_features_matrix[question_index][i] != has_feature:
                #eliminate from the board
                user_board[i][1] = False
        print("YOUR UPDATED BOARD:")
        print(user_board)
        
        
    '''CHECK IF WON AGAIN'''
    if num_in(user_board) == 1 or num_in(my_board) == 1:
        winner = game_finished(my_board, user_board, 0)
        break
    
    '''COMPUTER'S TURN'''
    
    comp_question_index = decision1(comp_features_matrix, my_board)
    print(f"I will look at {list_of_features[comp_question_index]}")
    
    if features_matrix[comp_question_index][users_choice_index] == 1:
        has_feature = 1
        #print answer
        print(f"yes, your person has {list_of_features[comp_question_index]}")
    else:
        has_feature = 0
        print(f"no, your person doesnt have {list_of_features[comp_question_index]}")
    
    #update the user's list of names
    for i in range(len(my_board)):
        if comp_features_matrix[comp_question_index][i] != has_feature:
            #eliminate from the board
            my_board[i][1] = False
    print("MY UPDATED BOARD:")
    print(my_board)


'''DECLARE THE WINNER'''


print(f"THE WINNER IS: {winner}")




'''
def update_board(choice_index, question_index, board, features_matrix, list_of_features):
    if features_matrix[question_index][choice_index] == 1:
        has_feature = 1
        #print answer
        print(f"yes, my person has {list_of_features[question_index]}")
    else:
        has_feature = 0
        print(f"no, my person doesnt have {list_of_features[question_index]}")

    #update the user's list of names
    for i in range(len(user_board)):
        if user_features_matrix[question_index][i] != has_feature:
            #eliminate from the board
            user_board[i][1] = False

'''
'''
class Decisions(object):
    @staticmethod
    def stdquestion (features):
        probabilities = []
        for feature in features:
            probability = 0
            nelim = 0
            for person in feature:
                if person == 1 or person == 0:
                    probability += person
                    nelim += 1
            probabilities.append(abs(probability/nelim - 0.5))

        to_ask = feature[min(probability)]
        return (to_ask)

    def expectedquestion(features, board):
        expected = []
        for feature in features:
            probability = 0
            nelim = 0
            num_feature = 0
            for person_index in feature:
                if board[person_index][1] == True:
                    nelim += 1
                        _______


class Player:
    #names: lost of names of character
    #questions:
    def __init__(self, computer_board, user_board, names, questions, features, decision):
        self.names = names
        self.questions = questions
        self.features = _____TODO_______

        self.user_card = ______
        self.board = [name: False for name in names]

    def load_feature_matrix()
        features = np.array([])
        for name in names
            #add the sql row of

    #the computer chooses what question to ask
    def ask_question(self):
        feature = Decisions.decision(self.features)
        #returns the feature we will enquire about
        return (feature)


    #updates board based on the opponents response
    def update_board(self, is_player = True):
        #call ask question ,
        if is_player:
            to_ask = input("Inquire about a feature:")
        else:
            to_ask = ask_question(self)


        #check if the user's name has this feature,
        if feature in user_card:
            for person in feature:
                if person == 0 and board[names[person]] == False:
                    board[names[person]] = True

        return board


while True:
   #Player chooses a question
   player_question = _______

   board = player.update_player_board(question, board, question_index)




  '''







