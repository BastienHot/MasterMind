#:author: Bastien Hottelet / Theo Bernaville
#:school: IUT Maubeuge
#:obj: Faire un MasterMind qui s'affiche dans la console, la combinaison est déterminée
# par l'ordinateur, les propostions sont faites par l'utilisateur, à la fin l'utilisateur
# peut décider de relancer ou arrêter de jouer.

#Importations
from random import randint
#On importe randint pour la valeur de la solution qui est donnée par la machine

#Notre classe qui contient le jeu
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
                         'orange':[4,'O'],'bleu':[5,'B'],'gris':[6,'G'],'blanc':[7,'W']}
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
        :info: Fonction qui prend en paramètre un objet de la classe MasterMind et qui affiche les
        couleurs disponibles selon ce que l'objet contient dans le dictionnaire self.param
        
        :param: objet de MasterMind
        :obj: afficher les couleurs disponibles
        :return: None
        '''
        #Initialisation d'un compteur pour une comparaison interne à la fonction 
        j:int
        j=0
        #Parcours du dictionnaire self.couleurs, on fait prendre à i la valeur de chaque élément
        for i in self.couleurs:
            print(i,end='')
            j+=1
            #Comparaison qui limite au nombre de couleurs voulues
            if(j>=self.param['Nombre_Couleur']):
                return
            #mise en page (après la comparaison pour éviter d'avoir une virgule à la fin)
            print(', ',end='')
        return
    
    #fonction qui permet de selectionner le nombre de couleur voulu pour la manche
    def changerNbrCouleur(self):
        '''
        :info: Fonction qui sert au parametrage et change la valeur de self.param['Nombre_Couleurs']
        
        :param: objet de MasterMind
        :obj: changer le nombre de couleurs utilisés (entre 4 et 8)
        :return: None
        '''
        #choix de nombre de couleur par l'utilisateur
        n = input('Veuillez entrer le nombre de couleurs pour cette manche (4 a 8) : ')
        #test erreur de saisie, si valide, execute la fonction a nouveau
        if(not n.isdigit() or int(n)>8 or int(n)<4):
            print('Votre réponse doit être un entier de 4 a 8')
            return self.changerNbrCouleur()
        else:
        #si aucune erreur, on change la variable
            self.param['Nombre_Couleur'] = int(n)
            return
    
    #fonction qui permet de selectionner le nombre d'essai voulu pour la manche
    def changerNbrEssai(self):
        '''
        :info: Fonction qui sert au parametrage et change une valeur de self.param,
        établit également la variable self.essai_restant qui sera égal à self.param
        au début puis subira -1 à chaque manche
        
        :param: objet de MasterMind
        :obj: changer le nombre d'essai que l'utilisateur a pour gagner la manche
        entre 12 et 14 inclus
        :return: None
        '''
        #choix de nombre d'essai par l'utilisateur
        n = input("Veuillez entrer le nombre d'essai pour cette manche (12 a 14) : ")
        #test erreur de saisie, si valide, execute la fonction a nouveau
        if(not n.isdigit() or int(n)>14 or int(n)<12):
            print('Votre réponse doit être un entier de 12 a 14')
            return self.changerNbrEssai()
        else:
        #si aucune erreur, on change la variable
            self.param['Nombre_Essais'] = int(n)
            self.nbr_essai_restant = int(n)
            return
        
    #fonction qui permet de selectionner le nombre de pions voulu pour la manche
    def changerNbrElem(self):
        '''
        :info: Fonction qui sert au parametrage et change une valeur de self.param
        
        :param: objet de MasterMind
        :obj: changer le nombre de pions utilisés pour la partie de MasterMind (4 à 5)
        :return: None
        '''
        #choix du nombre de pions par l'utilisateur
        n = input("Veuillez entrer le nombre de pions pour cette manche (4 a 5) : ")
        #test erreur de saisie, si valide, execute la fonction a nouveau
        if(not n.isdigit() or int(n)>5 or int(n)<4):
            print('Votre réponse doit être un entier de 4 a 5')
            return self.changerNbrElem()
        else:
        #si aucune erreur, on change la variable
            self.param['Nombre_Pions'] = int(n)
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
    def parametrage(self):
        '''
        :info: Fonction qui lance toute les fonctions de parametrage
        
        :param: objet de MasterMind
        :obj: recuperer toutes les valeurs nécessaire au déroulement de la manche :
        - self.param['Nombre_Pions'] -> nombre de pions (4 à 5)
        - self.param['Nombre_Couleur'] -> nombre de couleurs utilisés (4 à 8)
        - self.param['Essais'] -> nombre de manches (12 à 14)
        - self.tours -> dictionnaire qui stock les résultats des manches précédentes,
        initialisé selon le nombre de manches (self.nbr_essai)
        :return: None
        '''
        #changement du nombre de pions
        self.changerNbrElem()
        #changement du nombre de couleurs
        self.changerNbrCouleur()
        #changement du nombre d'essai
        self.changerNbrEssai()
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
    
    def guess(self):
        '''
        :info: Fonction qui demande la combinaison que le joueur propose
        
        :param: objet de MasterMind
        :obj: Demande une couleur pour chaque pions de la solution (4 à 5) pour que l'on puisse les comparer dans une autre fonction.
        Les couleurs sont entrées avec leur nom complet, exemple : "noir", "rouge", "bleu", "jaune" et une par une
        Si erreur de saisie, l'utilisateur reprend la ou l'erreur à été commise.
        A la fin, nous ajoutons la proposition au dictionnaire self.tours à la clé correspondante 
        :return: None
        '''
        if(len(self.player_guess)==0):
            print('')
            #affichage des couleurs possibles
            print("Les couleurs disponibles sont : ",end='')
            self.afficherCouleurs()
            print('')
        if(len(self.player_guess)<self.param['Nombre_Pions']):
            print("Veuillez entrer la couleur n°",len(self.player_guess)+1,"de votre combinaison : ",end='')
            n = input()
            #test erreur de saisie, si valide, execute la fonction a nouveau
            if(n.isdigit() or n not in self.couleurs or self.couleurs[n][0]>=self.param['Nombre_Couleur']):
                print("Mauvaise couleur")
                return self.guess()
            else:
            #si aucune erreur, on change la variable
                self.player_guess.append(self.couleurs[n][0])
            self.guess()
        else:
            self.nbr_essai_restant -= 1
            self.tours["Tour " + str(self.param['Nombre_Essais']-self.nbr_essai_restant)].append(self.player_guess)
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
    
def lancerJeu():
    '''
    :info: Fonction qui lance le jeu avec l'affichage client dans la console, permet de choisir les
    paramètres de la manche et de rejouer si voulu.

    :param: aucun
    :obj: Lancer toutes les fonctions qui permettent de jouer et s'occuper de l'affichage côté client
    :return: Aucun ou la fonction elle même pour relancer le jeu
    '''
    
    good_col:int
    good_pos:int
    #Couleurs entrées des tours précedents
    results:list
    #reponse rejouer ou non
    rep:str
    #creation de l'objet jeu
    jeu=MasterMind()
    #parametrage du jeu
    jeu.parametrage()
    #creation de la combinaison par l'ordinateur
    jeu.combi()
    #initialisation de good_pos pour la condition du Tant que
    good_pos=0
    #tentative de l'utilisateur
    while(jeu.nbr_essai_restant>0 and good_pos!=jeu.param['Nombre_Pions']):
        jeu.player_guess = []
        jeu.guess()
        jeu.nbrElemValide()
        if(jeu.nbr_essai_restant<jeu.param['Nombre_Essais']):
            print("--------------------------------------------------------")
            for i in range(jeu.param['Nombre_Essais']-jeu.nbr_essai_restant):
                #nombre de bonne couleur
                good_col = jeu.tours["Tour " + str(i+1)][1]
                #nombre de bonne position
                good_pos = jeu.tours["Tour " + str(i+1)][2]
                results = jeu.tours["Tour " + str(i+1)][0]
                print("Au tour",i+1,", vous avez entré les valeurs : ")
                for j in range(len(results)):
                    for k in jeu.couleurs:
                        if(jeu.couleurs[k][0]==results[j]):
                            print(jeu.couleurs[k][1], ' ', end = '')
                print('')
                print("vos résultats étaient")
                print(good_col, "bonne(s) couleur(s), mauvaise(s) position(s)")
                print(good_pos, "bonne(s) couleur(s), bonne(s) position(s)")
                print("--------------------------------------------------------")
    if(good_pos==jeu.param['Nombre_Pions']):
        print("Bravo, vous avez gagné la manche !")
        print("Voulez-vous jouer à nouveau ? (Y/n)")
        rep = input()
        if(rep=='Y'):
            lancerJeu()
        else:
            return
    else:
        print("Dommage, vous avez perdu la manche !")
        print("Voulez-vous jouer à nouveau ? (Y/n)")
        rep = input()
        if(rep=='Y'):
            lancerJeu()
        else:
            return

#si le programme est exécuté en tant que programme principal, on exécute la fonction lancerJeu()
if(__name__=="__main__"):
    lancerJeu()
        
        