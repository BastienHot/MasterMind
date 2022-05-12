#:author: Bastien Hottelet
#:school: IUT Maubeuge
#:obj: Create a MasterMind game displayed in the terminal, the secret code is determined
# by the human player, the propositions are given by the AI, which is either random or smart,
# at the end of each round the user gets to choose if he wants to play again or stop, if he
# decides to play one more round, we switch roles for the next one, if he decides to stop
# we thank him and the program stops

#Importations
#randint for the random solution
from random import randint
#MasterMind_Import for the MasterMind with opposite roles
import MasterMind_Import

class MasterMindIA():
    #Constructor of MasterMindIA class
    def __init__(self):
        self.colors:dict
        self.code:list
        #param -> [Pawn_Number, Colors_Number, Tries_Number]
        self.param:dict
        self.rounds:dict
        self.tries_left:int
        #Set of possibilities for smart resolution
        self.possibilities:list
        self.possibilities=[]
        #List of colors and the values assigned at each of them
        self.colors = {'black':[0,'Black'],'red':[1,'Red'],'green':[2,'Green'],'yellow':[3,'Yellow'],
                         'orange':[4,'Orange'],'blue':[5,'Blue'],'grey':[6,'Grey'],'white':[7,'White']}
        self.code=[]
        self.param={'Pawn_Number':0,'Colors_Number':0,'Tries_Number':0}
        self.tries_left=self.param['Pawn_Number']
        self.rounds={}
        
    # function used to change the number of pawns desired for the current round 
    def changeNbrPawns(self):
        '''
        :info: Function made to change the value of self.param (the number of pawns here)
        
        :param: object of MasterMindIA
        :obj: change the number of pawns used in the round (4 to 5)
        :return: None
        '''
        #choice of the number of pawns
        n = input("Please enter the desired numbers of pawns for this round (4 to 5) : ")
        #typing mistake verification, if a mistake is spotted, execute the function again after telling that there was a problem
        if(not n.isdigit() or int(n)>5 or int(n)<4):
            print('Your answer must be an interger between 4 and 5 !')
            return self.changeNbrPawns()
        else:
        #if no mistakes, we save the answer
            self.param['Pawn_Number'] = int(n)
            return
        
    # function used to change the number of colors desired for the current round 
    def changeNbrColors(self):
        '''
        :info: Function made to change the value of self.param (the number of colors here)
        
        :param: object of MasterMindIA
        :obj: change the number of colors used in the round (4 to 5)
        :return: None
        '''
        #choice of the number of colors
        n = input('Please enter the desired numbers of colors for this round (4 to 8) : ')
        #typing mistake verification, if a mistake is spotted, execute the function again after telling that there was a problem
        if(not n.isdigit() or int(n)>8 or int(n)<4):
            print('Your answer must be an interger between 4 and 8 !')
            return self.changeNbrColors()
        else:
        #if no mistakes, we save the answer
            self.param['Colors_Number'] = int(n)
            return
    
    #fonction qui permet de selectionner le nombre d'essai voulu pour la manche
    def changeNbrTries(self):
        '''
        :info: Function made to change the value of self.param (the number of tries here),
        also set the variable self.tries_left to self.param["Tries_Number"]
        
        :param: object of MastermindIA
        :obj: change the number of tries in the round (12 to 14)
        :return: None
        '''
        #choice of the number of tries
        n = input("Please enter the desired numbers of tries for this round (12 to 14) : ")
        #typing mistake verification, if a mistake is spotted, execute the function again after telling that there was a problem
        if(not n.isdigit() or int(n)>14 or int(n)<12):
            print('Your answer must be an interger between 12 and 14 !')
            return self.changeNbrTries()
        else:
        #if no mistakes, we save the answer
            self.param['Tries_Number'] = int(n)
            self.tries_left = int(n)-1
            return
        
    def setupRounds(self):
        '''
        :info: Function that initialize the dictionnary self.rounds, which keeps the data from
        every previous round
        
        :param: object of MastermindIA
        :obj: Initialize the dictionnary self.rounds
        :return: None
        '''
        for i in range(self.param['Tries_Number']):
            #in the future, the values of the list will be [AI code, good colors, good positions]
            self.rounds['Round '+ str(i+1)]=[]
        return
    
    #fonction qui permet le paramétrage
    def setup(self):
        '''
        :info: Fonction qui lance toute les fonctions de setup
        
        :param: object of MastermindIA
        :obj: recuperer toutes les valeurs nécessaire au déroulement de la manche :
        - self.param['Pawn_Number'] -> nombre de pions (4 à 5)
        - self.param['Colors_Number'] -> nombre de couleurs utilisés (4 à 8)
        - self.param['Essais'] -> nombre de manches (12 à 14)
        - self.rounds -> dictionnaire qui stock les résultats des manches précédentes,
        initialisé selon le nombre de manches (self.nbr_essai)
        :return: None
        '''
        #set up of the number of pawns
        self.changeNbrPawns()
        #set up of the number of colors
        self.changeNbrColors()
        #set up of the number of tries
        self.changeNbrTries()
        #setup of the rounds dictionnary 
        self.setupRounds()
        return
    
    #fonction qui demande la combinaison secrète du joueur
    def demanderCombi(self):
        '''
        :param: object of MastermindIA
        :obj: Sauvegarder la combinaison de l'utilisateur dans l'objet de classe MasterMindIA
        qui est en paramètre
        :return: None
        '''
        #Variables locales
        couleurs_dispo:list
        couleur_ajouter:str
        j:int
        couleurs_dispo=[]
        j=0
        #Affichage des couleurs disponibles selon les paramètres
        print('Les couleurs dispos sont : ', end='')
        for i in self.colors:
            if(j<self.param['Colors_Number']):
                j+=1
                couleurs_dispo.append(i)
        for k in range(len(couleurs_dispo)):
            print(couleurs_dispo[k], end='')
            if(k<len(couleurs_dispo)-1):
                print(', ', end='')
        print('')
        #Demande les couleurs à ajouter à la combinaison une par une
        for i in range(self.param['Pawn_Number']):
            couleur_ajouter = input("Entrez votre couleur n°" + str(len(self.code)+1) +" : ")
            while(couleur_ajouter not in couleurs_dispo):
                print("La couleur entrée doit être parmis les couleurs citées au-dessus !")
                couleur_ajouter = input("Entrez votre couleur n°" + str(len(self.code)+1) +" : ")
            #Ajout de la couleur à la combinaison
            self.code.append(self.colors[couleur_ajouter][0])
        return
    
    def comparer(self, combi:list)->tuple:
        '''
        :param: object of MastermindIA, combinaison de MasterMind sous forme de liste
        :obj: Compare la combinaison donnée en paramètre à la dernière combinaison soumise
        par l'algorithme. Sert notamment à l'élimination de toutes les solutions qui ne
        donnerait pas le même résultat
        :return: Tuple contenant les bonnes couleurs et bonnes positions
        '''
        #Variables locales
        guess:list
        temp_combi:list
        #compteurs de bonnes réponses
        good_position:int
        good_color:int
        #curseur de déplacement
        cur:int
        pos:int
        #Copie des listes pour éviter de modifier les listes originales
        temp_combi=combi.copy()
        guess=self.rounds["Tour " + str(self.param['Tries_Number']-self.tries_left-1)][0].copy()
        good_position = 0
        good_color = 0
        cur = 0
        pos = 0
        #parcours des listes et verification des bonnes positions
        while(cur<len(temp_combi)):
            if(guess[cur]==temp_combi[cur]):
                guess.pop(cur)
                temp_combi.pop(cur)
                good_position += 1
            else:
                cur+=1
        #reinitialisation du compteur
        cur=0
        #parcours des listes et verification des bonnes couleurs sans compter les bonnes positions
        while(cur<len(temp_combi)):
            if(guess[cur] in temp_combi):
                for i in range(len(temp_combi)):
                    if(temp_combi[i]==guess[cur]):
                        pos = i
                temp_combi.pop(pos)
                guess.pop(cur)
                good_color += 1
            else:
                cur+=1
        #retourne les bonnes couleurs et bonnes positions sous forme de tuple               
        return str(good_color),str(good_position)
    
    def demanderPlacement(self):
        '''
        :param: object of MastermindIA
        :obj: Demander le nombre de bonnes couleurs et bonnes positions de la combinaison soumise
        par l'ordinateur. Enregistre celle-ci dans self.rounds
        :return: None
        '''
        #Saisie du nombre de bonnes couleurs et bonnes positions de la solution affichée au dessus
        #quand nous lancons le code principale "lancerJeuJoueur()"
        good_col=input("Nombre de bonnes couleurs : ")
        good_pos=input("Nombre de bonnes positions : ")
        #Vérification du nombre de bonnes couleurs, doit être un entier entre 0 et Nombre Pions
        if(not good_col.isdigit() or int(good_col)>self.param['Pawn_Number'] or int(good_col)<0):
            print('Votre réponse doit être un entier de 0 a ' + str(self.param['Pawn_Number']))
            return self.demanderPlacement()
        else:
            #Vérification du nombre de bonnes positions, doit être un entier entre 0 et Nombre Pions
            if(not good_pos.isdigit() or int(good_pos)>self.param['Pawn_Number'] or int(good_pos)<0):
                print('Votre réponse doit être un entier de 0 a ' + str(self.param['Pawn_Number']))
                return self.demanderPlacement()
            else:                
                #Vérification du nombre de bonnes couleurs+bonnes positions, doit être un entier entre 0 et Nombre Pions
                if((int(good_col)+int(good_pos))>self.param['Pawn_Number']):
                    print('Vos réponses indiquent un trop grand nombre de pions, veuillez recommencer !')
                    return self.demanderPlacement()
                else:
                    #Vérification du verdict de l'utilisateur, si il est faux, nous le redemandons, sinon nous
                    #l'ajoutons à self.rounds
                    if(self.comparer(self.code)==(good_col,good_pos)):
                        self.rounds["Tour " + str(self.param['Tries_Number']-self.tries_left-1)].append(str(good_col))
                        self.rounds["Tour " + str(self.param['Tries_Number']-self.tries_left-1)].append(str(good_pos))
                    else:
                        print("Vous vous êtes trompé dans la saisie, veuillez recommencer ! ")
                        return self.demanderPlacement()
                    
    def randomGuess(self):
        '''
        :param: object of MastermindIA
        :obj: Sauvegarder une combinaison aléatoire dans self.rounds
        :return: None
        '''
        #Variables locales
        i:int
        random_guess:list
        random_guess=[]
        #Création d'une combinaison aléatoire
        for i in range(self.param['Pawn_Number']):
            random_guess.append(randint(0,self.param['Colors_Number']-1))
        #ajout de la combinaison à self.rounds
        self.rounds["Tour "+str(self.param['Tries_Number']-self.tries_left)].append(random_guess)

    def remplirIntelligent(self):
        '''
        :param: object of MastermindIA
        :obj: Remplir l'ensemble S des solutions possibles au MasterMind selon les
        paramètres de self.param, sauvegarde cela dans self.possibilities
        :return: None
        '''
        for i in range(self.param['Colors_Number']):
            for j in range(self.param['Colors_Number']):
                for k in range(self.param['Colors_Number']):
                    for l in range(self.param['Colors_Number']):
                        if(self.param['Pawn_Number']==4):
                            cur=i*self.param['Colors_Number']**3+j*self.param['Colors_Number']**2+k*self.param['Colors_Number']+l
                            self.possibilities.append([])
                            self.possibilities[cur].append(i)
                            self.possibilities[cur].append(j)
                            self.possibilities[cur].append(k)
                            self.possibilities[cur].append(l)
                        else:
                            for m in range(self.param['Colors_Number']):
                                cur=i*self.param['Colors_Number']**4+j*self.param['Colors_Number']**3+k*self.param['Colors_Number']**2+l*self.param['Colors_Number']+m
                                self.possibilities.append([])
                                self.possibilities[cur].append(i)
                                self.possibilities[cur].append(j)
                                self.possibilities[cur].append(k)
                                self.possibilities[cur].append(l)
                                self.possibilities[cur].append(m)
                                                                                    
    def intelligent(self):
        '''
        :param: object of MastermindIA
        :obj: Efface toutes les possibilités de combinaison qui ne donnent pas le même résultat
        que celle testée précédemment et défini la prochaine combinaison
        :return: None
        '''
        #Variables locales
        result:list
        comparaison:tuple
        new_possible:list
        #Prise en charge de la première tentative
        if(self.param['Tries_Number']-self.tries_left==1 and
           self.param['Pawn_Number']==5):
            combinaison=[0,0,1,1,1]
            
        elif(self.param['Tries_Number']-self.tries_left==1 and
             self.param['Pawn_Number']==4):
            combinaison=[0,0,1,1]
        #Prise en charge de la suite
        else:
            #Sauvegarde des résultats du tour précédent dans result
            new_possible=[]
            result=[]
            result.append(self.rounds["Tour "+str(self.param['Tries_Number']-
                                                 self.tries_left-1)][1])
            result.append(self.rounds["Tour "+str(self.param['Tries_Number']-
                                                 self.tries_left-1)][2])
            #Supression de toutes les possibilités qui ne donnerait pas le même résultat
            for i in range(len(self.possibilities)):
                comparaison=self.comparer(self.possibilities[i])
                if(comparaison[0]==result[0] and comparaison[1]==result[1]):
                    new_possible.append(self.possibilities[i])
            #Mise à jour de la liste des possibilités
            self.possibilities=new_possible
            #Définition de la prochaine combinaison
            combinaison=self.possibilities[0]
        self.rounds["Tour "+str(self.param['Tries_Number']-self.tries_left)].append(combinaison)
        
    def afficherGuess(self):
        '''
        :param: object of MastermindIA
        :obj: Afficher la combinaison soumise par l'ordinateur pour le tour en cours
        :return: None
        '''
        #Variables locales
        result:list
        combinaison:list
        result=[]
        combinaison=[]
        
        #Sauvegarde de la combinaison soumise par l'ordinateur dans result 
        for k in range(self.param['Pawn_Number']):
            for i in self.colors:
                if(self.colors[i][0]==self.rounds["Tour "+str(self.param['Tries_Number']-self.tries_left)][0][k]):
                    result.append(self.colors[i][1])
                    
        #Affichage de la combinaison soumise par l'ordinateur
        print("----------------------------------------------")
        print('Nous sommes actuellement au Tour n°' + str(self.param['Tries_Number']-self.tries_left))
        print("La combinaison soumise par l'ordinateur est :")
        for j in range(len(result)):
            print("\t ", result[j], end='')
        print('')
        print('----------------------------------------------')
        
        #Sauvegarde de la combinaison secrète du Joueur
        for o in range(self.param['Pawn_Number']):
            for p in self.colors:
                if(self.colors[p][0]==self.code[o]):
                    combinaison.append(self.colors[p][1])
                    
        #Affichage de la combinaison secrète du Joueur
        print('Votre combinaison secrète est : ', end='')
        for u in range(self.param['Pawn_Number']):
            print(combinaison[u],end=' ')
        print('')
        print("----------------------------------------------") 
            
def lancerJeuJoueur():
    '''
    :param: None
    :obj: Fonction principale, lance toutes les fonctions secondaires du
    MasterMind afin d'effectuer une partie complète, rotation de rôles
    à chaque nouvelle manche, possibilité d'arrêter de jouer à la fin
    de chaque manche. Choix de résolution Intelligente ou Aléatoire par
    l'ordinateur
    :return: None
    '''
    #Variables locales
    result:str
    rep:str
    type_jeu:str
    #Création de l'objet MasterMindIA
    m=MasterMindIA()
    #Paramétrage du MasterMind
    m.setup()
    #Définition de la combinaison secrète du Joueur
    m.demanderCombi()
    #Création de l'ensemble S contenant toutes les solutions possibles
    m.remplirIntelligent()
    
    #Choix du type d'IA pour résoudre le MasterMind
    type_jeu=input("Quel type d'IA voulez-vous ? (Intelligent/Aléatoire)\nRéponse : ")
    #Vérification des erreurs de saisie
    while(type_jeu not in ['Intelligent','Aléatoire']):
        print("Veuillez taper une réponse correcte ! ")
        type_jeu=input("Quel type d'IA voulez-vous ? (Intelligent/Aléatoire)\nRéponse : ")
        
    #Boucle d'une manche qui s'arrête une fois que le nombre d'essai tombe à 0
    while(m.tries_left>=0):
        #Choix du type de combinaison soumise par l'ordinateur en fonction de la réponse au type d'IA
        if(type_jeu=='Aléatoire'):
            m.randomGuess()
        else:
            m.intelligent()
        #Affichade de la tentative de l'ordinateur
        m.afficherGuess()
        #On retire 1 essai
        m.tries_left-=1
        #Demande du nombre de bonnes couleurs / positions de la tentative de l'ordinateur
        m.demanderPlacement()
        #Vérification de l'état de la partie (gagné ou pas encore)
        if(int(m.rounds["Tour "+str(m.param['Tries_Number']-m.tries_left-1)][2])==m.param['Pawn_Number']):
            result='win'
            m.tries_left=-1
        else:
            result='loose'
            
    #Si l'ordinateur gagne la partie, on le déclare vainqueur
    if(result=='win'):
        print("L'ordinateur a gagné la partie ! ")
    #Sinon on le déclare perdant
    else:
        print("L'ordinateur a perdu la partie ! ")
    #On demande si le joueur veut jouer une nouvelle manche
    print("Voulez-vous continuer à jouer ? (Y/n)")
    rep=input("Réponse : ")
    
    #Si sa réponse est oui, on Inverse les rôles
    while(rep not in ['Y','y','N','n']):
        print('Veuillez saisir une réponse correcte (Y/n) ! ')
        rep=input("Réponse : ")
    if(rep=='Y' or rep=='y'):
        print("Nous allons donc maintenant inverser les rôles ! ")
        MasterMind_Import.lancerJeu()
        lancerJeuJoueur()
        return
    #Sinon fin du programme et on remercie le Joueur d'avoir joué
    else:
        print("D'accord, merci d'avoir joué avec notre ordinateur, hâte de vous revoir ! ")

#Lancement de la fonction principale si le script est exécuté en tant que
#script principal
if(__name__=="__main__"):
    lancerJeuJoueur()