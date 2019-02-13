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


#ANALYSE USER

Users_list=[Datas[i][6] for i in range(len(Datas))]
Users_l = list(set(Users_list))

#Approche ou on compte le nombre de user apparaissant une fois dans les datas, 2 fois etc...
U_count=dict()
for u in Users_list :
    if u in U_count:
        U_count[u]+=1
    else:
        U_count[u]=1
Users_count_hist=U_count.values()
plt.hist(Users_count_hist,bins=300)
plt.title('Histogramme representant le nombre de user \n en fonction des apparitions')
plt.xlabel("Nombre d'apparitions")
plt.ylabel("Nombre de users")
plt.show()

print("Nombre moyen de review par user : ",np.mean(list(Users_count_hist)))
print("Nombre median de review par user : ",np.median(list(Users_count_hist)))


#Approche ou on compte le nombre d'occurence dans les datas par user
def hist_user():
    users_hist= []
    
    for i in range(len(Users_l)):
        for j in range(U_count[Users_l[i]]):
            users_hist.append(i)
            
            
    plt.hist(users_hist,bins=8298)
    plt.title('Histogramme representant le nombre apparition par user ')
    plt.xlabel("User")
    plt.ylabel("Nombre d'apparations")
    plt.show()
    return

#max : 192

#Approche moyenne sur user par feature (ou on a retire les lignes sans user : '')

def get_line_user(Datas):
    D=dict()
    for line in Datas:
        if line[6]!='':
            if line[6] not in D:
                D[line[6]]=[]
            D[line[6]].append(line)
    return D

def moy_user(L,i):
    tmp=np.array([float(L[j][i]) for j in range(len(L)) if len(L[j])>i ] )
    return np.mean(tmp)

def sigma_user(L,i):
    tmp=np.array([float(L[j][i]) for j in range(len(L)) if len(L[j])>i ] )
    return np.sqrt(np.var(tmp))


Dict_line_user=get_line_user(Datas)
Users_l.pop(Users_l.index('')) #retire l'user non existant

def plot_moy_user(Dict_line_user):
    for i in valeurs_etudiees[1:]:
        P=[]
        for u in Users_l:
            P.append(moy_user(Dict_line_user[u],i))
        #plt.plot(P,marker='+')
        x = [i for i in range(len(P))]
        x_note=[i for i in range(1,6)]
        plt.scatter(x,P,alpha=0.3,cmap=cm.Paired)
        plt.title("Moyenne de chaque note user pour "+Labels[i])
        plt.xlabel("User")
        plt.ylabel("Note sur 5")
        plt.show()
    return
#on remarque que beaucoup de user (509) on mis la note de 5.0 pour cette rubrique  overall(biais ?)


def plot_sigma_user_all(Dict_line_user): #Tous users confondus
    for i in valeurs_etudiees[1:]:
        P=[]
        for u in Users_l:
            P.append(sigma_user(Dict_line_user[u],i))
        #plt.plot(P,marker='+')
        print(len(P))
        x = [i for i in range(len(P))]
        plt.scatter(x,P,alpha=0.3,cmap=cm.Paired)
        plt.title("Ecart type de chaque note user pour "+Labels[i])
        plt.xlabel("User")
        plt.ylabel("Note sur 5")
        plt.show()
        print("Nb users ayant 2.0: ",P.count(2.0))
    return

def plot_sigma_user(Dict_line_user):#user apparaissant au moins 2 fois
    for i in valeurs_etudiees[1:]:
        P=[]
        for u in Users_l:
            if len(Dict_line_user[u])>1:
                P.append(sigma_user(Dict_line_user[u],i))
        #plt.plot(P,marker='+')
        print(len(P))
        x = [i for i in range(len(P))]
        plt.scatter(x,P,alpha=0.3,cmap=cm.Paired)
        plt.title("Ecart type de chaque note user pour "+Labels[i])
        plt.xlabel("User")
        plt.ylabel("Note sur 5")
        plt.show()
        print("Nb users ayant 2.0: ",P.count(2.0))
    return
#les personnes ayant un ecart type de 2 ont mis un 1 et un 5, c'est l'ecart type max possible


def plot_sigma_moy_user(Dict_line_user):
    user_sig_tot = [[] for u in Users_l]
    for i in valeurs_etudiees[1:-1]:
        for u in range(len(Users_l)):
            user_sig_tot[u].append(moy_user(Dict_line_user[Users_l[u]],i))
            
    i = valeurs_etudiees[-1]
    for u in range(len(Users_l)):
        user_sig_tot[u].append(moy_user(Dict_line_user[Users_l[u]],i))
        user_sig_tot[u]=np.sqrt(np.var(user_sig_tot[u]))
    x = [i for i in range(len(user_sig_tot))]
    plt.scatter(x,user_sig_tot,alpha=0.3,cmap=cm.Paired)
    plt.title("Ecart type des moyennes de chaque note user \npour toutes les review")
    plt.xlabel("User")
    plt.ylabel("Note sur 5")
    plt.show()
    
    return user_sig_tot

#certaines prsonnes ont de grands ecarts sur leur moyenne (soit notent serieusement, soit notent negligemment)