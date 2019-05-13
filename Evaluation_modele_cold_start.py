import numpy as np
import csv
import Algo_filtr_coll_item_cold_start as Algo

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





Datas_train, Datas_test, Datas_item, Datas_user = Algo.preprocessing(Datas)

def notes_predites(Datas_train,Datas_test):
    res = []
    for u in Datas_test :
        item = list(Datas_test[u].keys())[0]
        pred = Algo.prediction(item,u,Datas_item)
        res.append((Datas_test[u][item],pred))
    return res

list_tuples = notes_predites(Datas_train,Datas_test)

def mse(list_tuples):
    mse = 0
    for y1,y2 in list_tuples:
        mse += (y1-y2)**2
    
    return mse/len(list_tuples)
        
tuples = [(1,1.5),(4,3.8),(3.5,3.9)]
print("Mean square error (cold start system): ",mse(list_tuples))
