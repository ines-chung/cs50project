from math import *
import cs50
import numpy as np
import random


'''PREAMBLE'''

db = cs50.SQL("sqlite:///characters.db")

all_names = db.execute("SELECT name, id FROM characters")
#print (all_names)
#
my_board = np.array([[person["name"], True] for person in all_names])
user_board = np.array([[person["name"], True] for person in all_names])

#print(user_board)

list_of_features = ["hairpartition", "haircurly", "hat", "bald", "hairstuff", "hairlong", "hairginger", "hairwhite", "hairbrown", "hairblonde", "hairblack", "mouthbig", "nosebig", "cheeksred", "eyesblue", "sad", "hairfacial", "mustache", "beard", 'glasses', "earrings", "female"]
all_ = (db.execute("SELECT * FROM characters"))

print(all_[0])


features_matrix = []
i = 0
for feature in list_of_features:
    feature_lst = []
    for person in all_:
        feature_lst.append(person[feature])
    #print(feature_lst)
    features_matrix.append(feature_lst)

user_features_matrix = np.array(features_matrix)
comp_features_matrix = np.array(features_matrix)
print (user_features_matrix)


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

#the features of the card the user is trying to find.
#computers_choice_features = all_features[computers_choice_index]

#the features of the card we are trying to find
#users_choice_features = all_features[users_choice_index]

'''USER'S TURN'''
#index of the feature the user wants to question:
print(list_of_features)
question_index = int(input("What feature are you gonna ask about?"))

#Update the user's board

if features_matrix[question_index][computers_choice_index] == 1:
    has_feature = 1
    #print answer
    print(f"yes, my person is {list_of_features[question_index]}")
else:
    has_feature = 0
    print(f"no, my person isnt {list_of_features[question_index]}")

#update the user's list of names
for i in range(len(user_board)):
    if user_features_matrix[question_index][i] != has_feature:
        #eliminate from the board
        user_board[i][1] = False


'''COMPUTER'S TURN'''
#returns the index of the feature the computer is testing
def decision (board, features):
        probabilities = []
        for feature in features:
            probability = 0
            nelim = 0
            for i in range(len(feature)):
                if board[i][1] == True:
                    probability += person
                    nelim += 1
            probabilities.append(abs(probability/nelim - 0.5))

        to_ask = probabilities.index(min(probability))[0]
        return (to_ask)


comp_question_index = decision(my_board, comp_features_matrix)
print(f"I will look at {list_of_features[comp_question_index]}")

if features_matrix[question_index][computers_choice_index] == 1:
    has_feature = 1
    #print answer
    print(f"yes, your person has {list_of_features[comp_question_index]}")
else:
    has_feature = 0
    print(f"no, your person doesnt have {list_of_features[comp_question_index]}")

#update the user's list of names
for i in range(len(my_board)):
    if user_features_matrix[comp_question_index][i] != has_feature:
        #eliminate from the board
        my_board[i][1] = False



'''CHECK IF WON'''

def num_in(board)
    num_in = 0
    for card in board:
        if card[1] == True:
            num_in += 1
    return(num_in)

#check if someone has one card left.
def game_finished(board1, board2):
    num_in_1 = num_in(board1)
    if num_in_1 == 1:
        return (True, 0)
    num_in_2 = num_in(board2)
    if num_in_1 == 1:
        return (True, 1)
    else:
        return (False)




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
