""" 
1 : Prendre tous les utilisateurs qui ont noté plus d'une bière. 
2 : Mettre une de leur bière de côté et prédire la note qu'il a mise. 
3 : Stocker ça dans une liste de tuple (note,note_predite)
4 : Faire MSE sur la liste de tuple. 
"""

import numpy as np
import csv
import Algo_filtr_coll_item as Algo
from math import *

Data_csv=[]
f=open("beer_reviews.csv")
spamreader=csv.reader(f,delimiter=",")
for row in spamreader:
    Data_csv.append(np.array(row))
Labels=Data_csv.pop(0)
Datas=np.array(Data_csv)


#récuperation des bières    
Beers={Datas[i][-1]:Datas[i][10] for i in range(len(Datas)-1)}
Beers_id=list(Beers.keys())
#récuperation des utilisateurs
Users_list=[Datas[i][6] for i in range(len(Datas))]
Users = list(set(Users_list))

##User Based
##Datas_user=dict()
##for row in Datas:
##    id_b=row[-1]
##    id_u=row[6]
##    rev_over=row[3]
##    if id_u not in Datas_user:
##        Datas_user[id_u]=dict() 
##    if id_b not in Datas_user[id_u]:
##        Datas_user[id_u][id_b]=[]
##    Datas_user[id_u][id_b].append(float(rev_over))
##    

Datas_train = []
Datas_test = []
retire= []

Datas_item = Algo.preprocessing(Datas)

indices=np.random.permutation(len(Datas))

for i in indices:
    row=Datas[i]
    id_b=row[-1]
    if (len(Datas_item[id_b])>1) and (id_b not in retire):
        retire.append(id_b)
        Datas_test.append(row)
    elif (len(Datas_item[id_b])>1) and (id_b in retire):
        Datas_train.append(row)

Datas_train = np.array(Datas_train)
Datas_test = np.array(Datas_test)


Datas_item_train = Algo.preprocessing(Datas_train)

def notes_predites(Datas_train,Datas_test):
    res = []
    Datas_item = Algo.preprocessing(Datas_train)
    for i in range(len(Datas_test)):
        item = Datas_test[i][-1]
        user = Datas_test[i][6]
        pred = Algo.prediction(item,user,Datas_item)
        res.append((Datas_test[i][3],pred))
    return res

#list_tuples = notes_predites(Datas_train,Datas_test)

def mse(list_tuples):
    mse = 0
    for y1,y2 in list_tuples:
        mse += (y1-y2)**2
    
    return mse/len(list_tuples)
        
tuples = [(1,1.5),(4,3.8),(3.5,3.9)]
print(mse(tuples))
