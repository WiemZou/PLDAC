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
Beers=[int(Datas[i][-1]) for i in range(len(Datas)-1)]

#récuperation des utilisateurs
Users_list=[Datas[i][6] for i in range(len(Datas))]
Users = list(set(Users_list))


def preprocessing(Datas):
    Datas_item=dict()
    for row in Datas:
        id_b=row[-1]
        id_u=row[6]
        rev_over=row[3]
        if id_b not in Datas_item:
            Datas_item[id_b]=dict()
        if id_u not in Datas_item[id_b]:
            Datas_item[id_b][id_u]=[]
        Datas_item[id_b][id_u].append(float(rev_over))
    for item in Datas_item:
        for u in Datas_item[item] :
            Datas_item[item][u]=np.mean(np.array(Datas_item[item][u]))
    return Datas_item


Datas_item=preprocessing(Datas)
    
    
def calcul_similarite(i,j):
    prod_scal=0
    norm_i=np.linalg.norm(np.array(list(i.values())),ord=2)
    norm_j=np.linalg.norm(np.array(list(j.values())),ord=2)
    for user in i:
        if user in j:
            prod_scal+=i[user]*j[user]
    return prod_scal/(norm_i*norm_j)


def prediction(i,u,Datas):
    Datas_item = preprocessing(Datas)
    ri_moy = np.mean(np.array(list(Datas_item[i].values())))
    riu = 0
    sim_abs = 0
    for j in Datas_item:
        if (j!=i) and (u in Datas_item[j]):
            sim_ij = calcul_similarite(Datas_item[i],Datas_item[j])
            riu += sim_ij*(Datas_item[j][u]-ri_moy)
            sim_abs += abs(sim_ij)
    
    return ri_moy + riu/sim_abs
            
#Bière la plus notée : '11757' avec 2444 avis
