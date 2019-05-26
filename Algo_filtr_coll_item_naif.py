import numpy as np
import csv


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


def preprocessing(Datas):
    Datas_user=dict()
    Datas_item=dict()
    for row in Datas:
        id_b=row[-1]
        id_u=row[6]
        rev_over=row[3]
        if id_u not in Datas_user:
            Datas_user[id_u]=dict() 
        if id_b not in Datas_user[id_u]:
            Datas_user[id_u][id_b]=[]
        if id_b not in Datas_item:
            Datas_item[id_b]=dict()
        if id_u not in Datas_item[id_b]:
            Datas_item[id_b][id_u]=[]
        Datas_item[id_b][id_u].append(float(rev_over))
        Datas_user[id_u][id_b].append(float(rev_over))
    for item in Datas_item:
        for u in Datas_item[item] :
            Datas_item[item][u]=np.mean(np.array(Datas_item[item][u]))
    for user in Datas_user:
        for b in Datas_user[user] :
            Datas_user[user][b]=np.mean(np.array(Datas_user[user][b]))
    
    
    Datas_train = dict()
    Datas_test = dict()

    
    for user in Datas_user:
        beers=Datas_user[user]
        if len(Datas_user[user])>1 :
            i=0
            keys=list(beers.keys())
            find=False
            while i<len(beers) and not find: #verifie que biere est notée par plus d'une personne
                if len(Datas_item[keys[i]])>1:
                    find=True
                i+=1
            if find :
                Datas_test[user]={keys[i-1]:beers[keys[i-1]]}
                for j in range(len(beers)):
                    if j!=(i-1):
                        if keys[j] not in Datas_train:
                            Datas_train[keys[j]]=dict()
                        Datas_train[keys[j]][user]=Datas_item[keys[j]][user]
            else : #aucune biere notee plus de deux fois : on met la premiere
                Datas_test[user]={keys[0]:beers[keys[0]]}
                for j in range(1,len(beers)):
                        if keys[j] not in Datas_train:
                            Datas_train[keys[j]]=dict()
                        Datas_train[keys[j]][user]=Datas_item[keys[j]][user]
                        
        if len(Datas_user[user])==1 :
            keys=list(beers.keys())
            Datas_test[user]={keys[0]:beers[keys[0]]}                

    return Datas_train, Datas_test, Datas_item, Datas_user


Datas_train, Datas_test, Datas_item, Datas_user = preprocessing(Datas)

   

def prediction_naive(i,u,Datas_train):
    naif_overall=np.array([Datas_train[i][v] for v in Datas_train[i]])
    return np.mean(naif_overall)


def prediction_u_infos_naive(i,u_infos,Datas_item,Beers):
    if len(Datas_item[i])>500: #Il faut que la bière ait été noté bcp de fois pour qu'on la prenne en compte.
        naif_overall=np.array([Datas_item[i][v] for v in Datas_item[i] ])
        return np.mean(naif_overall)
    else :
        return 1


def select_pred(u_info,pred):
    i=0
    cpt=0
    res = []
    a = np.array([pred[i][1] for i in range(len(pred)) if pred[i][1]>1])
    print(len(a))
    while cpt<5:
        if Beers[pred[i][0]] not in u_info:
            res.append(pred[i])
            cpt+=1
        i+=1
    return res

def reco_5_beers(user_infos,Datas_item,Beers):
    pred=dict() 
    for beer in Beers:
        p=prediction_u_infos_naive(beer,user_infos,Datas_item,Beers)
        pred[beer]=p
        

    pred=sorted(pred.items(), key= lambda x:x[1],reverse=True)#pred.items() change le dictionnaire en list de couple (key,value), ensuite on trie cette liste selon les notes.
    print(pred[:5])
    return select_pred(user_infos,pred)

