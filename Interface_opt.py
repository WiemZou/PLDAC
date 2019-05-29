# Multi-frame tkinter application v2.3
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
from tkinter import *
from tkinter.messagebox import *
import numpy as np
import csv
import Algo_filtr_coll_item_cold_start_opt as Algo


Data_csv=[]
f=open("beer_reviews.csv")
spamreader=csv.reader(f,delimiter=",")
for row in spamreader:
    Data_csv.append(np.array(row))
Labels=Data_csv.pop(0)
global Datas 
Datas = np.array(Data_csv)



def traitement(texte):
    texte = texte.lower()
    texte = texte.strip()
    return texte
    
global Bd_Beers,Beers,Conversion, Beers_style, Beers_degree, Similarites

Beers = dict()
Beers_degree=dict()
Beers_style=dict()
Conversion = dict()
Bd_beers = []
Users_list = []

for i in range(len(Datas)-1):
    txt = traitement(Datas[i][10])
    Beers[Datas[i][-1]] = txt
    if Datas[i][-1] not in Beers_degree and len(Datas[i][-2])!=0:
        Beers_degree[Datas[i][-1]] = Datas[i][-2]
    if Datas[i][-1] not in Beers_style and len(Datas[i][7])!=0:
        Beers_style[Datas[i][-1]] = Datas[i][7]
        
    Conversion[txt] = Datas[i][-1]
    Bd_beers.append(txt)
    
    txt = traitement(Datas[i][6])
    Users_list.append(txt)
Bd_names = set(Users_list)
Bd_beers = set(Bd_beers)



#on considere que l'utilisateur connait deja le nom des bieres
global new_user,old_user,beer_courante
new_user = ''
old_user = ''
beer_courante=[]

def convert_user(u_infos):
    global Beers
    res = dict()
    for v in u_infos:
        new_v = Beers[v]
        res[new_v] = u_infos[v]
    return res

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one.""" 
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

def print_name(event):
    print(entree.get())


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
#        load = Image.open("BeerFlix.jpg") https://pythonbasics.org/tkinter-image/
#        render = ImageTk.PhotoImage(load)
        Label(self, text='Bienvenue chez Beerflix !',fg='red').pack(side="top", fill="x", pady=10)
        Button(self, text="Sign in",
                  command=lambda: master.switch_frame(SignIn)).pack()
        Button(self, text="Sign up",
                  command=lambda: master.switch_frame(SignUp)).pack()

class SignIn(Frame): #utilisateur existant
    def __init__(self, master):
        Frame.__init__(self, master)
        self.title="Beerzon"
        Label(self, text="Entrez votre nom d'utilisateur-trice").pack(side="top", fill="x", pady=10)

        value = StringVar(self)
        
        entree = Entry(self, textvariable=value, width=30)
        entree.pack()
        entree.focus_set()
        
        self.nom = entree

        Button(self, text="Ok",
                  command=lambda: self.dans_base(master)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()
    
    def dans_base(self,master):
        nom = self.nom.get()
        global Bd_names,old_user
        if nom not in Bd_names:
            showinfo('Attention',"Ce nom d'utilisateur n'existe pas. Si vous n'êtes pas enregistré veuillez cliquer sur SignUp pour créer un compte.")

        else :
            old_user = nom
            master.switch_frame(SignIn_entrer)

class SignUp(Frame): #nouvel utilisateur
    def __init__(self, master):
        Frame.__init__(self, master)
        self.title="Beerzon"
        Label(self, text="Entrez un nom d'utilisateur-trice \n").pack(side="top", fill="x", pady=10)

        value = StringVar(self)
        
        entree = Entry(self, textvariable=value, width=30)
        entree.pack()
        entree.focus_set()
        
        self.nom = entree

        Button(self, text="Ok",
                  command=lambda: self.dans_base(master)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()
    
    def dans_base(self,master):
        nom = self.nom.get()
        global Bd_names,new_user
        if nom in Bd_names:
            showinfo('Attention',"Ce nom d'utilisateur-trice existe déjà !")

        else :

            new_user = nom
            master.switch_frame(SignUp_entrer)



class SignUp_entrer(Frame): 
    def __init__(self, master):
        Frame.__init__(self, master)
        global new_user
        texte = "Bienvenue parmi nous " + new_user+ ' !'
        Label(self, text=texte).pack(side="top", fill="x", pady=10)
       
        Button(self, text="Se faire conseiller une bière",
          command=lambda: master.switch_frame(Naiv_advice)).pack()
        Button(self, text="Entrer la note d'une bière",
          command=lambda: master.switch_frame(new_user_note)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()

class SignIn_entrer(Frame): 
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Bienvenue parmi nous cher-ère amateur-trice de bières...").pack(side="top", fill="x", pady=10)
       
        Button(self, text="Se faire conseiller une bière",
          command=lambda: master.switch_frame(Beer_advice)).pack()
        Button(self, text="Entrer la note d'une bière",
          command=lambda: master.switch_frame(old_user_note)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()

def maj_new(nom,note,new_beer):
    global Datas,old_user,new_user,Bd_names,Bd_beers,Conversion,Beers,beer_courante
    
    texte = "La note " + note + " a été atrribuée à la " + nom +"."
    showinfo('Note saisie',texte)

    old_user = new_user 
    # Car l'old_user courant devient celui qui n'avait pas de note mais qui mtn en a une
    #FAIRE MISE A JOUR DES NOTES !
    Bd_names.add(new_user)
#Quoi faire ? Changer la grande base "Datas" et refaire un preprocessing à chaque recommandation ?

    tmp = list(Datas)
    liste = ['' for i in range(13)]
    tmp.append(liste)
    Datas = np.array(tmp)
    if nom in Conversion :
        Datas[-1][-1] = Conversion[nom]
    else :
        Conversion[nom]=nom
        Beers[nom]=nom
        Datas[-1][-1] = nom
    beer_courante.append(Conversion[nom])
    Datas[-1][10]=nom
    Datas[-1][6] = old_user
    Datas[-1][3] = note
    Datas = np.array(Datas)
    if new_beer == True:
        Bd_beers.add(nom)
    print(Datas[-1])
    return
    
class new_user_note(Frame): 
    def __init__(self, master):
        Frame.__init__(self, master)

        Label(self, text="Entrez le nom de la bière").pack(side ="top", fill="x", pady=10)

        value = StringVar(self)
        
        e1 = Entry(self, textvariable=value, width=30)
        e1.pack()
        e1.focus_set()
        self.nom = e1
        Label(self, text="Veuillez entrer la note de la bière entre 1 et 5 \n(Valeurs décimales possibles séparées par un '.')").pack(side="top", fill="x", pady=10)

        value = StringVar(self)
        
        e2 = Entry(self, textvariable=value, width=30)
        e2.pack()
        e2.focus_set()
        self.note = e2
  
    
        Button(self, text="Ok",
          command=lambda: self.test(master)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()
    def test(self,master):
        nom = traitement(self.nom.get())
        note = self.note.get()
        global Datas,old_user,new_user,Bd_names,Bd_beers,Conversion,Beers
        if nom in Bd_beers and float(note)<=5 and float(note)>=1:
            maj_new(nom,note,False)
            master.switch_frame(SignIn_entrer)
        elif not (float(note)<=5 and float(note)>=1):
            showinfo('Attention',"Veuillez noter la bière entre 1 et 5")
        else :
            if askyesno('Attention', "Vous êtes le premier à saisir une note pour cette bière, êtes vous certain-e de vouloir noter cette bière?'"):
                maj_new(nom,note,True)
                master.switch_frame(SignIn_entrer)
            else:
                rien_faire = 1

        return

def maj_old(nom,note,new_beer):
    global Datas,old_user,Bd_beers,Conversion,Beers,beer_courante
    
    texte = "La note " + note + " a été atrribuée à la " + nom.capitalize() +"."
    showinfo('Note saisie',texte)
    tmp = list(Datas)
    liste = ['' for i in range(13)]
    tmp.append(liste)
    Datas = np.array(tmp)
    if nom in Conversion :
        Datas[-1][-1] = Conversion[nom]
    else :
        Conversion[nom]=nom
        Beers[nom]=nom
        Datas[-1][-1] = nom
    beer_courante.append(Conversion[nom])
    Datas[-1][10]=nom
    Datas[-1][6] = old_user
    Datas[-1][3] = note
    Datas = np.array(Datas)
    if new_beer == True:
        Bd_beers.add(nom)
    return



class old_user_note(Frame): 
    def __init__(self, master):
        Frame.__init__(self, master)

        Label(self, text="Entrez le nom de la bière").pack(side ="top", fill="x", pady=10)

        value = StringVar(self)
        
        e1 = Entry(self, textvariable=value, width=30)
        e1.pack()
        e1.focus_set()
        self.nom = e1
        Label(self, text="Entrez la note de la bière entre 1 et 5 \n (Valeur décimale possible)").pack(side="top", fill="x", pady=10)

        value = StringVar(self)
        
        e2 = Entry(self, textvariable=value, width=30)
        e2.pack()
        e2.focus_set()
        self.note = e2
  
    
        # Faire old_user = new_user après que l'user ai donné au moins une note valide.
        Button(self, text="Ok",
          command=lambda: self.test(master)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()
    def test(self,master):
        nom = traitement(self.nom.get())
        note = self.note.get()
        global Datas,old_user,Bd_beers,Conversion,Beers
        if nom in Bd_beers and float(note)<=5 and float(note)>=1:
            maj_old(nom,note,False)
            master.switch_frame(SignIn_entrer)
        elif not (float(note)<=5 and float(note)>=1):
            showinfo('Attention',"Veuillez noter la bière entre 1 et 5")
        else :
            if askyesno('Titre 1', "Vous êtes le-la premier-ère à saisir une note pour cette bière, êtes vous certain-e de vouloir noter cette bière ?'"):
                maj_old(nom,note,True)
                master.switch_frame(SignIn_entrer)
            else:
                rien_faire = 1

        return


class Naiv_advice(Frame): 
    def __init__(self, master):
        #COPIER COLLER BEER_ADVICE ET POSER U_INFOS = {} !!!
        Frame.__init__(self, master)
        global Datas,Beers, Beers_style, Beers_degree, beer_courante
        Datas_item , Datas_user = Algo.preprocessing(Datas)
        u_infos = {}
        Algo.maj_similarites(beer_courante,Datas_item,Beers)
        beer_courante=[]
        pred = Algo.reco_5_beers(u_infos,Datas_item,Beers)
        texte = "On vous recommande les bières suivantes :\n\n"
        for beer,note in pred:
            note = str(round(float(note)*20))
            if beer in Beers_degree:
                if beer in Beers_style:
                    texte += Beers[beer].capitalize() +" à "+note+"%. \nStyle : "+Beers_style[beer]+", Degré "+Beers_degree[beer]+" \n\n"
                else:
                    texte += Beers[beer].capitalize() +" à "+note+"%.\n Degré "+Beers_degree[beer]+" \n\n"
            else:
                if beer in Beers_style:
                    texte += Beers[beer].capitalize() +" à "+note+"%. \nStyle : "+Beers_style[beer]+" \n\n"
                else:
                    texte += Beers[beer].capitalize() +" à "+note+"%\n\n"

        Label(self, text=texte).pack(side="top", fill="x", pady=10)

        Button(self, text="Entrer la note d'une bière",
          command=lambda: master.switch_frame(new_user_note)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()

class Beer_advice(Frame): 
    def __init__(self, master):
        Frame.__init__(self, master)
        global old_user,Datas,Beers, Beers_style, Beers_degree, beer_courante
        Datas_item , Datas_user = Algo.preprocessing(Datas)
        
        u_infos = convert_user(Datas_user[old_user])
        Algo.maj_similarites(beer_courante, Datas_item,Beers)
        beer_courante=[]

        pred = Algo.reco_5_beers(u_infos,Datas_item,Beers)
        texte = "On vous recommande les bières suivantes :\n\n"
        for beer,note in pred:
            note = str(round(float(note)*20))
            if beer in Beers_degree:
                if beer in Beers_style:
                    texte += Beers[beer].capitalize() +" à "+note+"%. \nStyle : "+Beers_style[beer]+", Degré "+Beers_degree[beer]+" \n\n"
                else:
                    texte += Beers[beer].capitalize() +" à "+note+"%. \n Degré "+Beers_degree[beer]+" \n\n"
            else:
                if beer in Beers_style:
                    texte += Beers[beer].capitalize() +" à "+note+"%. \nStyle : "+Beers_style[beer]+" \n\n"
                else:
                    texte += Beers[beer].capitalize() +" à "+note+"%\n\n"
        Label(self, text=texte).pack(side="top", fill="x", pady=10)

        Button(self, text="Entrer la note d'une bière",
          command=lambda: master.switch_frame(old_user_note)).pack()
        Button(self, text="Retour à l'accueil",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
app.mainloop()
