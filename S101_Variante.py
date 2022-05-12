#:author: Bastien Hottelet / Theo Bernaville
#:school: IUT Maubeuge
#:obj: Variante du MasterMind de S101_Main.py, mais en version graphique, tout sera affiché dans une
# fenêtre tkinter plutôt que dans la console

#Importations
from random import randint #On importe randint pour la valeur de la solution qui est donnée par la machine
from tkinter import * #On importe tkinter pour réaliser l'interface graphique du jeu
import time #On importe time pour pouvoir manipuler les update de tkinter sans en faire trop
import threading #On importe le threading pour certaines actions effectués par les boutons de tkinter

#Notre classe qui contient le jeu (partie technique)
class MasterMind():
    
    def __init__(self):
        #variable de classe
        #contient toutes les couleurs disponibles
        self.couleurs:dict
        #contient la solution
        self.elem:list
        #contient le nombre d'essai restant de l'utilisateur
        self.nbr_essai_restant:int
        #contient la proposition du joueur pour le tour en cours
        self.player_guess:list
        #dictionnaire qui contient l'historique des tours
        self.tours:dict
        #dictionnaire qui contient les paramètre de la manche
        self.param:dict
        
        #definition des variables de classe
        #dictionnaire avec les couleurs et leur valeurs correspondantes
        self.couleurs = {'noir':[0,'N'],'rouge':[1,'R'],'vert':[2,'V'],'jaune':[3,'J'],
                         'orange':[4,'O'],'bleu':[5,'B'],'gris':[6,'G'],'blanc':[7,'W'],
                         'violet':[8,'P'],'marron':[9,'M']}
        #liste qui contiendra la combinaison solution
        self.elem = []
        #liste qui contient la reponse de l'utilisateur
        self.player_guess = []
        #dictionnaire avec les resultats de chaque tour
        self.tours = {}
        #dictionnaire qui contient les paramètre de la manche
        self.param = {'Nombre_Pions':0, 'Nombre_Essais':0, 'Nombre_Couleur':0}
        
        
    #fonction d'affichage des couleurs et leur valeur correspondantes sous forme d'entier
    def afficherCouleurs(self):
        '''
        :info: Fonction qui prend en paramètre un objet de la classe MasterMind et qui renvoie les
        couleurs disponibles selon ce que l'objet contient dans le dictionnaire self.param
        
        :param: objet de MasterMind
        :obj: renvoie les couleurs disponibles
        :return: str_col-> type = string
        '''
        str_col:str
        str_col=""
        #Initialisation d'un compteur pour une comparaison interne à la fonction
        j:int
        j=0
        #Parcours du dictionnaire self.couleurs, on fait prendre à i la valeur de chaque élément
        for i in self.couleurs:
            str_col+=i
            j+=1
            #Comparaison qui limite au nombre de couleurs voulues
            if(j>=self.param['Nombre_Couleur']):
                return str_col
            #mise en page (après la comparaison pour éviter d'avoir une virgule à la fin)
            str_col+=', '
    
    #fonction qui permet de selectionner le nombre de couleur voulu pour la manche
    def changerNbrCouleur(self, nbr:int):
        '''
        :info: Fonction qui sert au parametrage et change la valeur de self.param['Nombre_Couleurs']
        en fonction de ce que contient le paramètre 'nbr'
        
        :param: objet de MasterMind, nbr -> type='int'
        :obj: changer le nombre de couleurs utilisés (entre 4 et 10)
        :return: None
        '''
        #prise en charge de cas incorrects
        assert int(nbr)>=4 and int(nbr)<=10, "Le chiffre doit être un entier compris entre 4 et 8"
        self.param['Nombre_Couleur'] = int(nbr)
        return
    
    #fonction qui permet de selectionner le nombre d'essai voulu pour la manche
    def changerNbrEssai(self, nbr:int):
        '''
        :info: Fonction qui sert au parametrage et change une valeur
        de self.param en fonction de ce que contient le paramètre nbr,
        établit également la variable self.essai_restant qui sera égal
        à self.param au début puis subira -1 à chaque manche
        
        :param: objet de MasterMind, nbr -> type='int'
        :obj: changer le nombre d'essai que l'utilisateur a pour gagner la manche
        entre 12 et 20 inclus
        :return: None
        '''
        #prise en charge de cas incorrects
        assert int(nbr)>=12 and int(nbr)<=20, "Le chiffre doit être un entier compris entre 12 et 20"
        self.param['Nombre_Essais'] = int(nbr)
        self.nbr_essai_restant = int(nbr)
        return
        
    #fonction qui permet de selectionner le nombre de pions voulu pour la manche
    def changerNbrElem(self,nbr):
        '''
        :info: Fonction qui sert au parametrage et change une valeur de self.param en
        fonction de ce que contient le paramètre nbr
        
        :param: objet de MasterMind, nbr -> type='int'
        :obj: changer le nombre de pions utilisés pour la partie de MasterMind (4 à 6)
        :return: None
        '''
        #prise en charge de cas incorrects
        assert int(nbr)>=4 and int(nbr)<=6, "Le chiffre doit être un entier compris entre 4 et 6"
        self.param['Nombre_Pions'] = int(nbr)
        return
    
    def setupTours(self):
        '''
        :info: Fonction qui initialise le dictionnaire self.tours, dictionnaire qui stock
        les résultats des manches précédentes
        
        :param: objet de MasterMind
        :obj: mettre en place la configuration de base du dictionnaire de résultats des manches
        :return: None
        '''
        for i in range(self.param['Nombre_Essais']):
            #dans le futur, les valeurs de la liste seront [combinaison utilisateur, nombre couleurs ok, nombre positions ok]
            self.tours['Tour '+ str(i+1)]=[]
        return
    
    #fonction qui permet le paramétrage
    def parametrage(self, nbr1:int, nbr2:int, nbr3:int):
        '''
        :info: Fonction qui lance toute les fonctions de parametrage
        
        :param: objet de MasterMind, / nbr1, nbr2, nbr3, tous de type='int'
        :obj: recuperer toutes les valeurs nécessaire au déroulement de la manche :
        - self.param['Nombre_Pions'] -> nombre de pions (4 à 6)
        - self.param['Nombre_Couleur'] -> nombre de couleurs utilisés (4 à 10)
        - self.param['Essais'] -> nombre de manches (12 à 20)
        - self.tours -> dictionnaire qui stock les résultats des manches précédentes,
        initialisé selon le nombre de manches (self.nbr_essai)
        :return: None
        '''
        #changement du nombre de pions
        self.changerNbrElem(nbr1)
        #changement du nombre de couleurs
        self.changerNbrCouleur(nbr2)
        #changement du nombre d'essai
        self.changerNbrEssai(nbr3)
        #mise en place des tours
        self.setupTours()
        return
    
    #fonction qui determine la combinaison
    def combi(self):
        '''
        :info: Fonction qui crée la combinaison du côté ordinateur et la stock dans self.elem
        
        :param: objet de MasterMind
        :obj: Créer une combinaison de chiffres qui correspondent à des couleurs, combinaison qui
        sera celle que le joueur doit deviner (stocké dans self.elem).
        :return: None
        '''
        #boucle nombre d'elem
        for i in range(self.param['Nombre_Pions']):
            #choix aleatoire de la combinaison
            self.elem.append(randint(0,self.param['Nombre_Couleur']-1))
        return
    
    def nbrElemValide(self):
        '''
        :info: Fonction qui compare les positions données par l'utilisateur à celle
        de la combinaison solution
        
        :param: objet de MasterMind
        :obj: Savoir le nombre de positions correctes et de couleurs correctes, les ajoutes au
        dictionnaire self.tours pour stocker les résultats.
        :return: None
        '''
        #Variables locales
        #doublons des listes de combinaisons
        pos_temp_combi:list
        pos_temp_guess:list
        #compteurs de bonnes réponses
        good_position:int
        good_color:int
        #curseur de déplacement
        cur:int
        pos:int
        pos_temp_combi = self.elem.copy()
        pos_temp_guess = self.player_guess.copy()
        good_position = 0
        good_color = 0
        cur = 0
        pos = 0
        #parcours des listes et verification des bonnes positions
        while(cur<len(pos_temp_combi)):
            if(pos_temp_guess[cur]==pos_temp_combi[cur]):
                pos_temp_guess.pop(cur)
                pos_temp_combi.pop(cur)
                good_position += 1
            else:
                cur+=1
        #reinitialisation du compteur
        cur=0
        #parcours des listes et verification des bonnes couleurs sans compter les bonnes positions
        while(cur<len(pos_temp_combi)):
            if(pos_temp_guess[cur] in pos_temp_combi):
                for i in range(len(pos_temp_combi)):
                    if(pos_temp_combi[i]==pos_temp_guess[cur]):
                        pos = i
                pos_temp_combi.pop(pos)
                pos_temp_guess.pop(cur)
                good_color += 1
            else:
                cur+=1
        #ajout des résultats dans notre dictionnaire des tours                
        self.tours["Tour " + str(self.param['Nombre_Essais']-self.nbr_essai_restant)].append(good_color)
        self.tours["Tour " + str(self.param['Nombre_Essais']-self.nbr_essai_restant)].append(good_position)
        return
    
#Notre class qui contient le jeu (partie graphique)
class Fenetre():
    '''
    :info: Fenetre de jeu du MasterMind
            Nom en haut, au milieu
            Première étape: Paramètrage de la manche à l'aide de curseur Scale de tkinter
            Deuxième étape: Tentatives de l'utilisateur pour deviner la combinaison de l'ordinateur
            Troisièe étape: Choix de relancer ou non selon deux boutons
            Oui -> Reset la fenêtre, retour à l'étape 1 / Non -> Ferme la fenêtre, fin de l'exécution
        
    '''
    def __init__(self, dimx=1920, dimy=1080):
        '''
        :info: Constructeur de la classe Fenetre, permet de créer la fenêtre qui servira à l'affichage graphique
                stock également un grand nombre de conteneur destinés à l'affichage futur de parties principales
                du déroulement du jeu
        
        :param: dimensions, si non précisez, 1920x1080
        :obj: créer la fenêtre tkinter pour l'interface graphique
        :return: None
        '''
        self.window = Tk(screenName="MasterMind")
        self.window.geometry(str(dimx)+'x'+str(dimy))
        self.title_frame = Frame(self.window, borderwidth=2)
        self.title_frame.pack(side=TOP)
        self.mainframe = Frame(self.window, borderwidth=2)
        self.mainframe.pack(anchor='center', pady=100)
        self.color_frame = Frame(self.window, borderwidth=2)
        self.color_frame.pack(side=BOTTOM, pady=20)
        self.title = Label(self.title_frame, text = "MasterMind", font=("Arial",30,'underline','bold'))
        self.title.pack()
        self.scale_elem:Scale
        self.scale_couleurs:Scale
        self.scale_essai:Scale
        self.scale_button:Button
        self.scale_res:list
        self.scale_res=[]
    
    
    def pressButton(self, master, button:str):
        '''
        :info: Est appelé par les boutons de couleurs de l'interface graphique tkinter
        
        :param: master -> objet de la classe MasterMind() / button -> str renvoyé par un bouton de couleur tkinter 
        :obj: sauvegarder les propositions de l'utilisateurs, les enregistres couleur par couleur dans la liste
        player_guess de l'objet de la classe MasterMind, et affiche les couleurs sélectionnés au fur et à mesure
        :return: None
        '''
        master.player_guess.append(int(button))
        for i in master.couleurs:
            if(master.couleurs[i][0]==int(button)):
                couleur=i
        if(len(master.player_guess)==master.param['Nombre_Pions']):
            self.color_frame.destroy()
            self.color_frame = Frame(self.window, borderwidth=2)
            self.color_frame.pack(side=BOTTOM, pady=20)
        else:
            couleur=Label(self.color_frame, text='Couleur n°' + str(len(master.player_guess)) + ' : ' + couleur)
            couleur.pack()
        return
    
    def scale(self):
        '''
        :info: Affiche les curseurs permettant de définir les paramètres de la manche
        
        :param: Objet de la classe Fenetre 
        :obj: Permettre à l'utilisateur de sélectionner les paramètres de la manche
        :return: None
        '''
        #Nombre de pions
        self.scale_elem = Scale(self.mainframe, orient='horizontal', from_=4, to=6,
                           resolution=1, tickinterval=1, length=700,
                           label='Nombre de Pions', font=('Arial',20))
        self.scale_elem.pack(pady=30)
        #Nombre de couleurs
        self.scale_couleurs = Scale(self.mainframe, orient='horizontal', from_=4, to=10,
                           resolution=1, tickinterval=1, length=700,
                           label='Nombre de Couleurs', font=('Arial',20))
        self.scale_couleurs.pack(pady=30)
        #Nombre d'essais
        self.scale_essai = Scale(self.mainframe, orient='horizontal', from_=12, to=20,
                           resolution=1, tickinterval=1, length=700,
                           label="Nombre d'essai", font=('Arial',20))
        self.scale_essai.pack(pady=30)
        return
    
    def scaleButton(self):
        '''
        :info: Bouton qui permet de valider les paramètres de la manche et qui redirige vers une fonction
        qui les sauvegarde
        
        :param: Objet de la classe Fenetre
        :obj: Crée et affiche le bouton qui permet de passer à l'étape suivante et de sauvegarder les valeurs
        :return: None
        '''
        #bouton valider scale
        self.scale_button = Button(self.mainframe, text="Valider", font=('Arial',30),
                              command=self.recupScale)
        self.scale_button.pack(side=BOTTOM, pady=10, padx=10)
        return
        
        
    def recupScale(self):
        '''
        :info: Déclanché par scaleButton(self) de la classe Fenetre 
        
        :param: Objet de la classe Fenetre
        :obj: Sauvegarde les valeurs de paramétrage au moment de l'appui sur le bouton de validation
        et supprime chaque curseur après avoir récuperé ses infos
        :return: None
        '''
        self.scale_res.append(self.scale_elem.get())
        self.scale_elem.destroy()
        self.scale_res.append(self.scale_couleurs.get())
        self.scale_couleurs.destroy()
        self.scale_res.append(self.scale_essai.get())
        self.scale_essai.destroy()
        self.scale_button.destroy()
        return
    
    def afficherCouleurs(self, master):
        '''
        :info: Crée et affiche les boutons nécessaires au jeu 
        
        :param: Objet de la classe Fenetre, Objet de la classe MasterMind
        :obj: Crée et affiche les boutons qui permettent de faire une proposition sur ce que pourrait être
        la combinaison secrète
        :return: None
        '''
        i:int
        list_button:list
        list_size_frame:list
        color:list
        color = ['black','red','green','yellow','orange','blue','grey','white','purple','brown']
        list_button=[]
        list_size_frame=[]
        frame_button=Frame(self.mainframe)
        frame_button.pack(side=BOTTOM)
        for i in range(1,master.param['Nombre_Couleur']+1):
            list_size_frame.append("sizeframe"+str(i))
            list_button.append("button"+str(i))
            list_size_frame[i-1] = Frame(frame_button, height=75, width=75)
            list_size_frame[i-1].pack_propagate(0)
            list_size_frame[i-1].pack(side=LEFT,pady=20, padx=20)
            list_button[i-1] = Button(list_size_frame[i-1], bg=color[i-1],
                                      command=lambda name=str(i-1): threading.Thread(target = self.pressButton(master,name)).start())
            list_button[i-1].pack(fill=BOTH, expand=1)
        return
    
    def guess(self, master, color:str):
        '''
        :info: Fonction qui demande la combinaison que le joueur propose
        
        :param: objet de Fenetre, objet de MasterMind, string qui contient les couleurs dipsonibles
        :obj: afficher les couleurs possibles, réceptionne la propostion du joueur, actualise la fenêtre
         et a la fin, nous ajoutons la proposition au dictionnaire self.tours à la clé correspondante 
        :return: None
        '''
        available_col:str
        request:str
        #affichage des couleurs possibles
        available_col = "Les couleurs disponibles sont : " + color
        available_col_lab = Label(self.mainframe, text=available_col, font=('Arial',20))
        available_col_lab.pack(pady=10)
        request = "Veuillez appuyer sur les boutons correspondants \n aux couleurs que vous voulez"
        request_lab = Label(self.mainframe, text=request, font=('Arial',20))
        request_lab.pack(pady=10)
        while len(master.player_guess)!=master.param['Nombre_Pions']:
            time.sleep(0.01)
            self.window.update()
        self.mainframe.destroy()
        self.mainframe = Frame(self.window, borderwidth=2)
        self.mainframe.pack(anchor='center',pady=100)
        master.nbr_essai_restant -= 1
        master.tours["Tour " + str(master.param['Nombre_Essais']-master.nbr_essai_restant)].append(master.player_guess)
        return
    
def lancerJeu():
    '''
    :info: Fonction qui lance le jeu avec l'affichage client dans une interface graphique, permet de choisir les
    paramètres de la manche et de rejouer si voulu.
        
    :param: aucun
    :obj: Lancer toutes les fonctions qui permettent de jouer et s'occuper de l'affichage côté client
    :return: None
    '''
    combinaison:str
    #Lancement Fenetre
    f = Fenetre()
    
    #Lancement MasterMind
    jeu=MasterMind()
    
    #demande des paramètres de la manche
    f.scale()
    f.scaleButton()
    while(len(f.scale_res)!=3):
        f.window.update()
        time.sleep(0.01)
        
    #parametrage du jeu
    jeu.parametrage(f.scale_res[0], f.scale_res[1], f.scale_res[2])
    
    #creation de la combinaison par l'ordinateur
    jeu.combi()
    
    #initialisation de good_pos pour la condition du Tant que
    good_pos=0
    
    #initialisation des couleurs dispos
    color = jeu.afficherCouleurs()
    
    #config de l'affichage de resultats
    principal_frame= Frame(f.window, borderwidth=2, height=250,width=200)
    principal_frame.pack(side=BOTTOM, anchor='se')
    canvas_graph=Canvas(principal_frame, borderwidth=2, height=250,width=200)
    canvas_graph.pack(side=RIGHT)
    frame_graph=Frame(canvas_graph)
    
    #configuration du scroll dans les résultats
    s = Scrollbar(principal_frame, orient='vertical', command=canvas_graph.yview)
    s.pack(side=RIGHT, fill='y', expand=True)
    canvas_graph.config(yscrollcommand=s.set)
    canvas_graph.create_window((4,4), window=frame_graph, anchor="e", tags="frame_graph")
    frame_graph.bind("<Configure>", lambda x: canvas_graph.configure(scrollregion=canvas_graph.bbox("all")))
    
    
    top = Label(frame_graph, text="----------------------")
    top.pack(side=TOP)
    #tentative de l'utilisateur
    while(jeu.nbr_essai_restant>0 and good_pos!=jeu.param['Nombre_Pions']):
        #Paramètrage de base de la fenêtre
        f.afficherCouleurs(jeu)
        f.window.update()
        jeu.player_guess = []
        f.guess(jeu,color)
        jeu.nbrElemValide()
        #Tant que l'utilisateur a des essais restants
        if(jeu.nbr_essai_restant<jeu.param['Nombre_Essais']):
            #nombre de bonne couleur
            good_col = jeu.tours["Tour " + str(jeu.param['Nombre_Essais']-jeu.nbr_essai_restant)][1]
            #nombre de bonne position
            good_pos = jeu.tours["Tour " + str(jeu.param['Nombre_Essais']-jeu.nbr_essai_restant)][2]
            results = jeu.tours["Tour " + str(jeu.param['Nombre_Essais']-jeu.nbr_essai_restant)][0]
            at_round = Label(frame_graph, text="Tour "+str(jeu.param['Nombre_Essais']-jeu.nbr_essai_restant))
            at_round.pack(side=TOP,pady=5,padx=5)
            combinaison=""
            for j in range(len(results)):
                for k in jeu.couleurs:
                    if(jeu.couleurs[k][0]==results[j]):
                        combinaison += jeu.couleurs[k][1]+ " "
            combi_lab = Label(frame_graph, text= combinaison)
            combi_lab.pack(side=TOP,pady=5,padx=5)
            col= Label(frame_graph, text= str(good_col)+" bonne(s) couleur(s)")
            pos= Label(frame_graph, text= str(good_pos)+" bonne(s) position(s)")
            col.pack(side=TOP,pady=5,padx=5)
            pos.pack(side=TOP,pady=5,padx=5)
            bot = Label(frame_graph, text="----------------------")
            bot.pack(side=TOP,pady=5,padx=5)
    #reinitialisation du cadre principal pour afficher l'écran de fin
    f.mainframe.destroy()
    f.mainframe = Frame(f.window, borderwidth=2)
    f.mainframe.pack(anchor='center',pady=100)
    principal_frame.destroy()
    
    #Choix de la phrase à afficher selon les résultats de l'utilisateur
    if(good_pos==jeu.param['Nombre_Pions']):
        win_label= Label(f.mainframe, text="Bravo, vous avez gagné la manche ! \n Voulez vous rejouer ?", font=('Arial',25))        
        win_label.pack()
    else:
        lose_label=Label(f.mainframe, text="Dommage, vous avez perdu la manche ! \n Voulez vous rejouer ?", font=('Arial',25))
        lose_label.pack()
    
    #boutons de réponses de l'utilsateur / rejouer ou non
    rep_yes = Button(f.mainframe, text="Oui", font=('Arial',20), command=lambda:[f.window.destroy(), lancerJeu()])
    rep_no = Button(f.mainframe, text="Non", font=('Arial',20), command=f.window.destroy)
    rep_yes.pack(side=LEFT)
    rep_no.pack(side=RIGHT)
    
    #mainloop en attendant sa réponse
    f.window.mainloop()


#si le programme est exécuté en tant que programme principal, on exécute la fonction lancerJeu()
if(__name__=="__main__"):
    lancerJeu()
