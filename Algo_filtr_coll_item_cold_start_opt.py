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
Beers_infos=dict()
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

    return  Datas_item, Datas_user

#Sign up
#Nabil
#'Sausa Weizen' 5
#Datas.append(['' for i in range(11)])
#Datas[-1][-1] = id_be

Datas_item, Datas_user = preprocessing(Datas)

   
def calcul_similarite(i,j):
    prod_scal=0
    norm_i=np.linalg.norm(np.array(list(i.values())),ord=2)
    norm_j=np.linalg.norm(np.array(list(j.values())),ord=2)
    for user in i:
        if user in j:
            prod_scal+=i[user]*j[user]
    return prod_scal/(norm_i*norm_j)


fichier = open("similarites.txt","r")
global Similarites
Similarites = dict()
for ligne in fichier:
    b1,b2,sim = ligne.split(',')
    sim = float(sim.split('\n')[0])
    if b1 not in Similarites:
        Similarites[b1]=dict()
    Similarites[b1][b2]=sim
fichier.close()

def maj_similarites(l,tab,Beers): #tab=Datas_item
    global Similarites
    for item in l:
        if item not in Similarites:#nouvel item
            Similarites[item]=dict()
        for b in Beers:
            sim=calcul_similarite(tab[item],tab[b])
            Similarites[item][b]=sim
            if b in Similarites:
                Similarites[b][item]=sim

            
def seuil_similarite(Datas_train):
    s=0
    l=[]
    cpt = 0
    for b1 in Datas_train:
        for b2 in Datas_train:
            if b1!=b2 :
                sim=Similarites[b1][b2]
                if sim!=0:
                    s+=sim
                    l.append(sim)
                else:cpt+=1
            else:
                cpt += 1
    return s/(len(Datas_train)**2-cpt),l

#seuil_sim,l=seuil_similarite(Datas_train)
seuil_sim=0.1565987066635957

def new_calcul_sim(Datas_item,b1):
    for b2 in Datas_item:
        Similarites[b1][b2]=calcul_similarite(Datas_item[b1],Datas_item[b2])
        
    return

def prediction(i,u,Datas_train):
    global Similarites
    if len(Datas_user[u])==1:
        if len(Datas_item[i])==1:
            Rev_overall=np.array([Datas_train[k][v] for k in Datas_train for v in Datas_train[k]])
            return np.mean(Rev_overall)
        else:
            ri_moy = np.mean(np.array(list(Datas_train[i].values())))
            return ri_moy
    elif len(Datas_item[i])==1:
        Rev_overall=np.array([Datas_train[k][v] for k in Datas_train for v in Datas_train[k]])
        return np.mean(Rev_overall)
    
    ri_moy = np.mean(np.array(list(Datas_train[i].values())))
    riu = 0
    sim_abs = 0

    for j in Datas_train: #parcourt tous les items
        if (j!=i):
            if u in Datas_train[j]: #cas ou l'utilisateur a noté l'item j
                sim_ij = Similarites[i][j]
                if sim_ij >=seuil_sim:
                    riu += sim_ij*(Datas_train[j][u]-ri_moy)
                    sim_abs += abs(sim_ij)
    #ajouté
    if sim_abs==0: #cas ou user pas assez similaire (cold start)
        if len(Datas_item[i])==1:
            Rev_overall=np.array([Datas_train[k][v] for k in Datas_train for v in Datas_train[k]])
            return np.mean(Rev_overall)
        else:
            ri_moy = np.mean(np.array(list(Datas_train[i].values())))
            return ri_moy                              
    return ri_moy + riu/sim_abs
            
#Bière la plus notée : '11757' avec 2444 avis
#'csiewert' a noté 3 bières

#print(prediction('11757','csiewert',Datas_train))


def prediction_u_infos(i,u_infos,Datas_item,Beers):
    global Similarites
    ri_moy = np.mean(np.array(list(Datas_item[i].values())))
    riu = 0
    sim_abs = 0
    for v in u_infos:
        k=list(Beers.keys())[list(Beers.values()).index(v)]
        if (k!=i):
            sim_ij = Similarites[i][k]
            
            if sim_ij >=seuil_sim:
                riu += sim_ij*(u_infos[v]-ri_moy)
                sim_abs += abs(sim_ij)
    if sim_abs == 0:
        if len(Datas_item[i])==1:
            Rev_overall=np.array([float(Datas[i][3]) for i in range(len(Datas))])
            return np.mean(Rev_overall)
        else:
            ri_moy = np.mean(np.array(list(Datas_item[i].values())))
            return ri_moy                
    return ri_moy + riu/sim_abs   

 
#u_infos={'Sausa Weizen':2.5,'Caldera Ginger Beer':1.5,'Amstel Light':3.3}
u_infos={'Sausa Weizen':2.5,'Caldera Ginger Beer':1.5,'Amstel Light':3.3,'Founders Breakfast Stout':2.1,'Pilsner Urquell Kvasnicový (Unfiltered Yeast Beer)':2,'Irie IPA':1.5}

def select_pred(u_info,pred,Beers):
    i=0
    cpt=0
    res = []
    while cpt<5:
        if Beers[pred[i][0]] not in u_info:
            res.append(pred[i])
            cpt+=1
        i+=1
    return res


def reco_5_beers(user_infos,Datas_item,Beers):
    import time
    pred=dict()
    if len(user_infos)==0:
        for beer in Beers:
            if len(Datas_item[beer])>500 :
                p=np.mean(np.array([Datas_item[beer][v] for v in Datas_item[beer]]))
                pred[beer]=p
            else:
                pred[beer]=1
        pred=sorted(pred.items(), key= lambda x:x[1],reverse=True)
        return pred[:5]
            
    times = []
    for beer in Beers:
        p=prediction_u_infos(beer,user_infos,Datas_item,Beers)
        pred[beer]=p

    pred=sorted(pred.items(), key= lambda x:x[1],reverse=True)#pred.items() change le dictionnaire en list de couple (key,value), ensuite on trie cette liste selon les notes.
    return select_pred(user_infos,pred,Beers)
