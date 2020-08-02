from math import *
import numpy as np
import random



'''PREAMBLE'''

db = cs50.SQL("sqlite:///characters.db")
all_names = db.execute("SELECT name, id FROM characters")
#print (all_names)
board1 = [{person["name"], True} for person in all_names]
board2 = np.array([[person["name"], True] for person in all_names])
print (board1["Anne"])

all_features =  db.execute("SELECT name, mouth, nose, cheeks_rosy, eyes, hair_color, hair_length, hair_texture, hair_midpart, glasses, earrings, hat, wrinkles, hair_facial  FROM characters")


for person in all_features:
    if person["mouth"] == 'large':
        person["mouth"] = 1
    else:
        person["mouth"] = 0
    if person["nose"] == 'large':
        person["nose"] = 1
    else:
        person["nose"] = 0
    if person["eyes"] == 'blue':
        person["eyes"] = 1
    else:
        person["eyes"] = 0
    if person["mouth"] == 'large':
        person["mouth"] = 1
    else:
        person["mouth"] = 0

#ourboard
board = np.array([name:id:])
#userboard
userboard = np.array([names])
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

    '''@staticmethod
    def expected (features):
        expectations = []
        for feature in features:
            num_with = 0
            num_without = 0
            nelim = 0
            for person in features:

    '''


class Player:
    #names: lost of names of character
    #questions:
    def __init__(self, board, names, questions, features, decision = std):
        self.names = names
        self.questions = questions
        self.features = load_features_matrix(names)
        #load the features of that user into the user's card.
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
    def update_board(self, response):
        #call ask question ,
        to_ask = ask_question(self)

        has_attribute = 1 or 0???

        #check if the user's name has this feature,
        if feature in user_card:
            for person in feature:
                if person == 0 and board[names[person]] = False:
                    board[names[person]] = True

        return board
