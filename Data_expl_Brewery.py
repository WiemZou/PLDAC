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


#MOYENNEs ET ECART-TYPES
#review time
def time(Datas):
    Rev_time=np.array([int(Datas[i][2]) for i in range(len(Datas))])
    moy_time=np.mean(Rev_time)
    sigma_time=np.sqrt(np.var(Rev_time))
    X_time= np.random.randn(100000) * sigma_time + moy_time
    plt.hist(X_time, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des review time de moyenne \n'+str(round(moy_time,2)))
    plt.grid()
    plt.show()
    return

#review overall (note sur 5)
def overall(Datas):
    Rev_overall=np.array([float(Datas[i][3]) for i in range(len(Datas))])
    moy_overall=np.mean(Rev_overall)
    sigma_overall=np.sqrt(np.var(Rev_overall))
    X_overall= np.random.randn(100000) * sigma_overall + moy_overall
    plt.hist(X_overall, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des notes globales de moyenne \n'+str(round(moy_overall,2))+' et ecart type '+str(round(sigma_overall,2)))
    plt.grid()
    plt.show()
    return

#review aroma (note sur 5)
def aroma(Datas):
    Rev_aroma=np.array([float(Datas[i][4]) for i in range(len(Datas))])
    moy_aroma=np.mean(Rev_aroma)
    sigma_aroma=np.sqrt(np.var(Rev_aroma))
    X_aroma= np.random.randn(100000) * sigma_aroma + moy_aroma
    plt.hist(X_aroma, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des notes arome de moyenne \n'+str(round(moy_aroma,2))+' et ecart type '+str(round(sigma_aroma,2)))
    plt.grid()
    plt.show()
    return

#review_appearance (note sur 5)
def appearance(Datas):
    Rev_app=np.array([float(Datas[i][5]) for i in range(len(Datas))])
    moy_app=np.mean(Rev_app)
    sigma_app=np.sqrt(np.var(Rev_app))
    X_app= np.random.randn(100000) * sigma_app + moy_app
    plt.hist(X_app, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des notes apparence de moyenne\n'+str(round(moy_app,2))+' et ecart type '+str(round(sigma_app,2)))
    plt.grid()
    plt.show()
    return

#review_palate (note sur 5)
def palate(Datas):
    Rev_palate=np.array([float(Datas[i][8]) for i in range(len(Datas)-1)])
    moy_palate=np.mean(Rev_palate)
    sigma_palate=np.sqrt(np.var(Rev_palate))
    X_palate= np.random.randn(100000) * sigma_palate + moy_palate
    plt.hist(X_palate, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des notes palais de moyenne\n'+str(round(moy_palate))+' et ecart type '+str(round(sigma_palate,2)))
    plt.grid()
    plt.show()
    return

#review_taste (note sur 5)
def taste(Datas):
    Rev_taste=np.array([float(Datas[i][9]) for i in range(len(Datas)-1)])
    moy_taste=np.mean(Rev_taste)
    sigma_taste=np.sqrt(np.var(Rev_taste))
    X_taste= np.random.randn(100000) * sigma_taste + moy_taste
    plt.hist(X_taste, bins=50, normed=1,color="lightblue")
    plt.title('Loi normale asssociee a la \ndistriution des notes gout de moyenne\n'+str(round(moy_taste))+' et ecart type '+str(round(sigma_taste,2)))
    plt.grid()
    plt.show()
    return

#ETUDE PAR MARQUE

Brewery={Datas[i][1] for i in range(len(Datas))}

#Recuperation des indices pour chaque brewery
D = dict()
for marque in Brewery :
    D[marque] = []
for i in range(len(Datas)):
    marque = Datas[i][1]
    D[marque].append(i) 
    
Brewery_list=list(Brewery)
Brewery_count=[len(D[marque]) for marque in Brewery_list]
Brewery_hist= []
for i in range(len(Brewery_list)):
    for j in range(len(D[Brewery_list[i]])):
        Brewery_hist.append(i)

plt.hist(Brewery_hist,bins=267)
plt.title('Histogramme des occurences des differentes Brasseries')
plt.show()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------"
 
#ETUDE du brewery ayant le plus de lignes
Nom_max_occ_brew=Brewery_list[Brewery_count.index(max(Brewery_count))]

#extraction des lignes associees
data_max = Datas[D[Nom_max_occ_brew]]

Beer_style = {data_max[i][7] for i in range(len(data_max))}
Beer_style_list = list(Beer_style)
S = dict()
for style in Beer_style :
    S[style] = []
for i in range(len(data_max)):
    S[data_max[i][7]].append(data_max[i])

def moy_sig(Datas,j):
    Rev=np.array([float(Datas[i][j]) for i in range(len(Datas))])
    moy=np.mean(Rev)
    sigma=np.sqrt(np.var(Rev))
    
    return moy,sigma

valeurs_etudiees = [2,3,4,5,8,9]

def moyennes_sigmas(Datas):
    moy = []
    sig = []
    for j in valeurs_etudiees :
        moy_inter , sig_inter = moy_sig(Datas,j)
        moy.append(moy_inter)
        sig.append(sig_inter)
    return moy,sig

moy_max,sig_max = moyennes_sigmas(data_max)

moy_styles = []
sig_styles = []
for style in Beer_style_list:
    moy_inter,sig_inter = moyennes_sigmas(S[style])
    moy_styles.append(moy_inter)
    sig_styles.append(sig_inter)    

list_moy_categorie = np.array(moy_styles).T
list_sig_categorie = np.array(sig_styles).T

def list_ecart_type(list_moy_categorie): 
    sigma = []
    for list_moy in list_moy_categorie:
        sigma.append(np.sqrt(np.var(list_moy)))
    return sigma

#Pas tres parlant, regardons si deux moyennes s'eloignent fortement 

def list_max_ecart(list_moy_categorie): #Un peu plus parlant, on sait qu'entre deux styles particulier il y a une grande difference
    list_ecart = []
    
    for list_moy in list_moy_categorie:
        max_ecart = 0
        for val1 in range(len(list_moy)):
            for val2 in range(len(list_moy)):
                ecart = abs(list_moy[val1]-list_moy[val2])
                if max_ecart < ecart:
                    max_ecart = ecart
                    i = val1
                    j = val2
        list_ecart.append((max_ecart,i,j))
    return list_ecart


#Etudions les Brawery une par une :
def time_moy(Datas):
    Rev_time=np.array([int(Datas[i][2]) for i in range(len(Datas))])
    moy_time=np.mean(Rev_time)
    return moy_time

#review overall (note sur 5)
def overall_moy(Datas):
    Rev_overall=np.array([float(Datas[i][3]) for i in range(len(Datas))])
    moy_overall=np.mean(Rev_overall)  
    return moy_overall

#review aroma (note sur 5)
def aroma_moy(Datas):
    Rev_aroma=np.array([float(Datas[i][4]) for i in range(len(Datas))])
    moy_aroma=np.mean(Rev_aroma)
    return moy_aroma

#review_appearance (note sur 5)
def appearance_moy(Datas):
    Rev_app=np.array([float(Datas[i][5]) for i in range(len(Datas))])
    moy_app=np.mean(Rev_app)
 
    return moy_app

#review_palate (note sur 5)
def palate_moy(Datas):
    Rev_palate=np.array([float(Datas[i][8]) for i in range(len(Datas)-1)])
    moy_palate=np.mean(Rev_palate)
  
    return moy_palate 

#review_taste (note sur 5)
def taste_moy(Datas):
    Rev_taste=np.array([float(Datas[i][9]) for i in range(len(Datas)-1)])
    moy_taste=np.mean(Rev_taste)

    return  moy_taste

moy_brewery = []
moy_brewery.append([time_moy(Datas[D[i]]) for i in Brewery_list ])
moy_brewery.append([overall_moy(Datas[D[i]]) for i in Brewery_list ])
moy_brewery.append([aroma_moy(Datas[D[i]]) for i in Brewery_list ])
moy_brewery.append([appearance_moy(Datas[D[i]]) for i in Brewery_list ])
moy_brewery.append([palate_moy(Datas[D[i]]) for i in Brewery_list ])    
moy_brewery.append([taste_moy(Datas[D[i]]) for i in Brewery_list ])

ecart =  list_max_ecart(moy_brewery)  #Le maximum difference de moyennes entre deux brasseries
