#import pandas
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm


##Data_pandas=pandas.read_csv("beer_reviews.csv",delimiter=",",index_col="brewery_id") Index premiere colonne
#Data_pandas=pandas.read_csv("beer_reviews.csv",delimiter=",")
#Labels_pandas=list(Data_pandas)

Data_csv=[]
f=open("beer_reviews.csv")
spamreader=csv.reader(f,delimiter=",")
for row in spamreader:
    Data_csv.append(np.array(row))
Labels=Data_csv.pop(0)
Datas=np.array(Data_csv)


valeurs_etudiees = [2,3,4,5,8,9]


#ANALYSE ITEM
    
Beers=[int(Datas[i][-1]) for i in range(len(Datas)-1)]
#Users_l = list(set(Users_list))

plt.hist(Beers,bins=1000)
plt.title("Histogramme representant le nombre d'apparition de chaque biere")
plt.xlabel("Id biere")
plt.ylabel("Nombre d'apparition")
plt.show()


B_count=dict()
for b in Beers :
    if b in B_count:
        B_count[b]+=1
    else:
        B_count[b]=1
Beers_count_hist=B_count.values()
plt.hist(Beers_count_hist,bins=300,range=[0,200])
plt.title("Histogramme representant le nombre de\n bieres en fonction du nombre d'apparition ")
plt.xlabel("Nombre d'apparition")
plt.ylabel("Nombre de bieres")
plt.show()

print("Nombre moyen de review par bière : ",np.mean(list(Beers_count_hist)))
print("Nombre median de review par bière : ",np.median(list(Beers_count_hist)))

def KeyByValue(dico,value):
    res = []
    for key in dico.keys():
        if dico[key] == value:
            res.append(key)
    return res

def moy_sig_liste_users(liste,j): 
    note = []
    for i in range(len(Datas)-1):
        if int(Datas[i][-1]) in liste:
            note.append(float(Datas[i][j]))
    if len(note)==0:
        return 0,0
    note = np.array(note)
    return np.mean(note),np.sqrt(np.var(note))

def moyenne_par_occ(j): #moyenne/sig des bieres apparaissant n fois
    values = [i for i in range(1,2200)]
    moyennes = dict()
    sigmas = dict()
    for value in values :
        res = KeyByValue(B_count,value)
        if len(res) != [] :
            moyennes[value],sigmas[value] = moy_sig_liste_users(res,j)
    return moyennes,sigmas

#moy,sig = moyenne_par_occ(3) 

#for i in range(1,2200): #Faire un graphique avec ca , Une courbe pour moyenne et une pour ecart type , ca prends une minute a charger
#    if moy[i] != 0:
#        print(i, "   ",moy[i],"    ",sig[i])





