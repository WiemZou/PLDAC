import csv
import numpy as np

Data_csv=[]
f=open("beer_reviews.csv")
spamreader=csv.reader(f,delimiter=",")
for row in spamreader:
    Data_csv.append(np.array(row))
Labels=Data_csv.pop(0)
Datas=np.array(Data_csv)
print('ici')

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
              

    return Datas_item, Datas_user
Datas_item, Datas_user = preprocessing(Datas)
def calcul_similarite(i,j):
    prod_scal=0
    norm_i=np.linalg.norm(np.array(list(i.values())),ord=2)
    norm_j=np.linalg.norm(np.array(list(j.values())),ord=2)
    for user in i:
        if user in j:
            prod_scal+=i[user]*j[user]
    return prod_scal/(norm_i*norm_j)

print("debut")
Similarites=dict()
for b1 in Datas_item:
    Similarites[b1]=dict()
    for b2 in Datas_item:
        if b1!=b2:
            if b2 in Similarites and b1 in Similarites[b2]:
                Similarites[b1][b2]=Similarites[b2][b1]
            else:
                sim=calcul_similarite(Datas_item[b1],Datas_item[b2])
                Similarites[b1][b2]=sim
                
print("fin")



fichier = open("similarites.txt", "w")
for b1 in Similarites :
    for b2 in Similarites[b1] :
        fichier.write(b1+","+b2+","+str(Similarites[b1][b2])+"\n")

fichier.close()

