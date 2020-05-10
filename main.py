import networkx as nx
import community
import numpy as np
import pyrebase
from flask import *
#import random

#config = {
  #"apiKey": "kk-z5PD3fWDDo",
  #"authDomain": "drinkonected.firebaseapp.com",
  #"databaseURL": "https://drinkonected.firebaseio.com",
  #"projectId": "drinkonected",
 # "storageBucket": "drinkonected.appspot.com",
#}

#def colorMaps(number_of_colors):
#    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#             for i in range(number_of_colors)]
#    return color

def makeMatrix(friends, allUser):
    nbUser = len(friends)
    matrix = np.zeros((nbUser, nbUser))

    for i in range (len(matrix)):
        for j in range(len(matrix)):
            if i != j :
                for ami in friends.get(allUser[i]):
                    if allUser[j] in ami:
                        #print(allUser[j] +' is friend of ' + allUser[i])
                        matrix[i,j] = 1
                    else :
                        #print(allUser[j] +' is nottt friend of ' + allUser[i])
                        matrix[i,j] = -1
    return matrix

def louvain(allUser,matrix):
    comm = {}
    graphPACT = nx.Graph()
    for i in range (len(matrix)):
        for j in range(len(matrix)):
            if(matrix[i,j] == 1):
                graphPACT.add_edges_from([(i, j)])

    #first compute the best partition
    partitionPACT = community.best_partition(graphPACT)
    number_of_colors = len(set(partitionPACT.values()))
    #colors=colorMaps(number_of_colors)
    colors= ['#98F856', '#FCF6D2', '#710934', '#65D199', '#CAF6F2', '#17BD0E', '#34A151', '#518BC8', '#22DC42']
    while number_of_colors > len(colors):
        newColor = '#FF'+ (len(colors)-number_of_colors)*1000
        colors.append(newColor)

    for k in partitionPACT :
        #print(str(partitionPACT[k]) + usercolor[partitionPACT[k]])
        #comm.update({allUser[k]: str(partitionPACT[k])})
        userColor = colors[partitionPACT[k]]
        comm.update({ allUser[k] : userColor })

    return comm

def getFirebaseUser():
    config = {
      "apiKey": "kkd",
      "authDomain": "test-7a615.firebaseapp.com",
      "databaseURL": "https://test-7a615.firebaseio.com",
      "projectId": "test-7a615",
      "storageBucket": "test-7a615.appspot.com",
    }

    firebase = pyrebase.initialize_app (config)
    db = firebase.database()
    users = db.child("users").get()
    friends = {}
    allUser={}
    cpt=0

    for user in users.each():
        metPpl = []
        userKey= user.key()
        allUser.update({cpt:userKey})
        cpt += 1
        data = db.child('users').child(userKey).child('metPeople').get()
        if data.val() is not None:
            for key, value in data.val().items():
                metPpl.append(value)

        friends.update({userKey: metPpl})
    return friends, allUser

def communityLouvain(userID):
    friends, allUser = getFirebaseUser()
    matrix = makeMatrix(friends, allUser)
    result=louvain(allUser, matrix)
    return (result.get(userID))

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Welcome to PACT 4.2 Drink'O'Neccted!"

@app.route("/getCommunity")
def get_community():
    userID = request.args.get("id")
    user_community = communityLouvain(userID)
    return user_community

if __name__ == "__main__":
    app.run(debug=True)
