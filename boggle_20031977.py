###############################################################################
## Programme qui simule une version simplifiee du jeu Boggle.
###############################################################################
## Auteur: Patrick Dube
## Copyright: Copyright 2023, boggle_20031977.py
## Version: 1.0.0
## Date: 08/03/23
## Email: patrick.dube.3@umontreal.ca
###############################################################################

# Déclaration des imports et dépendances
import random

# Déclaration des variables globales, constantes
grille = []
joueurs = []
liste_mots_joueurs = []
mots_rejettes = []
des_choisis = []
des = {
    1: 'ETUKNO', 
    2: 'EVGTIN', 
    3: 'DECAMP', 
    4: 'IELRUW', 
    5: 'EHIFSE', 
    6: 'RECALS', 
    7: 'ENTDOS', 
    8: 'OFXRIA',
    9: 'NAVEDZ', 
    10: 'EIOATA',
    11: 'GLENYU',
    12: 'BMAQJO',
    13: 'TLIBRA',
    14: 'SPULTE',
    15: 'AIMSOR',
    16: 'ENHRIS',
    17: 'ATSIOU',
    18: 'WIREBC',
    19: 'QDAHAU',
    20: 'ACFLNE',
    21: 'PRSTUG',
    22: 'JPRXEZ',
    23: 'EKVYBE',
    24: 'ALCHEM',
    25: 'EDUFHK'
}

# Déclaration des fonctions internes et calculs 
# avec commentaires détaillés nécessaires seulement (optionnel)

def generer_grille(taille):
    # empeche de prendre un de plus dune fois
    while len(des_choisis) < taille:
        de_random = des[random.randint(1, taille**2)]
        if de_random not in des_choisis:
            des_choisis.append(de_random)
    
    # construction de la grille a partir dune liste de des choisis contenant des des uniques
    for ligne in range(taille):
        grille.append([])
        for de in des_choisis:
            faceDe = de[random.randint(0, 5)]
            grille[ligne].append(faceDe)

    return grille

def generer_joueurs(nb_joueurs):
    for joueur in range(int(nb_joueurs)):
        liste_mots_joueurs.append([])
        joueur_actuel = {
            "numero" : joueur + 1,
            "mots" : liste_mots_joueurs[joueur]
        }
        joueurs.append(joueur_actuel)
    return joueurs

def afficher_grille(grille):
    for ligne in grille:
        # top line de ----------- a chaque new line (pattern = (4 * size) + 1)
        print('-' * (len(grille) * 4) + '-')
        # le | manquant du debut de chaque ligne de la premiere colonne puisquon ne fait que mettre un ' |' apres chaque element (il manque donc celui du debut avant chaque premier element de chaque ligne)
        print('|', end=' ')
        for lettre in ligne:
            print(lettre + ' |', end=' ')
        print()
    # bottom line de ------------ (vu quon met la top line dans la loop, il va manquer une derniere ligne de -------------)
    print('-' * (len(grille) * 4) + '-')

# IDEA: passer un dict joueur en param pour avoir acces a sa liste de mots et tous ses autres attributs
def afficher_pointage(grille, joueurs):   
    
    # IDEA: faire un for loop pour passer tous les joueurs 
    # PAR CONTRE: il faut aussi un affichage pour un seul joueur
    
    mots_joueurs_actuel = liste_mots_joueurs[numero_joueur - 1]
    longueur_mot_plus_long = len(max(mots_joueurs_actuel, key=len))
    longueur_base = 29 # longueur dune ligne dans lexemple
    longueur_reste = 18 # longueur dune ligne sans le mot
    longueur_totale = longueur_mot_plus_long + longueur_reste
    
    print(f"JOUEUR {numero_joueur}")
    # AFFICHAGE -----------------, width de 29 comme dans lexemple du prof (minimum), plus au besoin
    if longueur_totale > longueur_base:
        print('-'*longueur_totale)
    else:
        print('-'*longueur_base)
    
    # AFFICHAGE - MOT       (POINT) -- DECISION
    for mot in mots_joueurs_actuel:
        print('- ', end='')
        
        # mention ILLEGAL
        if est_valide(grille, mot):
            mention_illegal = ""
        else:
            mention_illegal = " -- ILLEGAL "

        # TODO: implementer la mention -- REJETER
        
        # ajustement de laffichage, centrer en un point fixe
        if len(mot) == longueur_mot_plus_long:
            print(mot + ' ' + f'({calcul_point(grille, mot)})' + f'{mention_illegal}')
        else:
            print(mot + ' ' + ' '*(longueur_mot_plus_long - len(mot)) + f'({calcul_point(grille, mot)})' + f'{mention_illegal}')
    
    #AFFICHAGE ========
    if longueur_totale > longueur_base:
        print('='*longueur_totale)
    else:
        print('='*longueur_base)
    
    #AFFICHAGE TOTAL
    print(f"TOTAL: {calcul_point(grille, mots_joueurs_actuel)}")

# TODO: verifier si le mot nest pas deja trouve par un autre joueur -- en faire une autre fonction et lappeler dans jouer()?   
def est_valide(grille, mot):
    # un mot est valide quand:
    # 1. same column
    # 2. same line
    # 3. adjacent letters, but not necessarily same line or same column (BONUS)
    # 4. le mot nest pas deja trouve
    
    valide = True
    # on verifie que chaque lettre est presente dans la grille
    
    # PROBLEME avec cette facon de faire: la loop prend la premiere lettre quil trouve, alors
    # en cas de duplicate, ce nest pas necessairement la bonne lettre et est_valide retourne FAUX alors
    # que ca devrait etre VRAI

    # Pour regler le probleme il faut continue de passer au travers la grille malgre 
    # la condition insatisfaite pour detecter une meme lettre qui pourrait satisfaire 
    # les conditions

    # Autre probleme: la loop pourrait rencontrer une premiere lettre duplicate et donc le reste des lettres ne sont pas adjacentes,
    # mais elles sont en realites adjacentes a la meme lettre dans une autre position de la grille

    # Autre probleme: exemple: TEST -- la loop reprend la position du 1er T pour le 2e T

    i = 0
    for letter in mot:
        for row in grille:
            if letter in row:
                if i == 0:
                    global xInitial, yInitial
                    xInitial = row.index(letter)
                    yInitial = grille.index(row)
                    valide = True
                    break
                # non seulement la lettre doit etre contenue dans
                else:
                    # ici on sait quon a pas la premiere lettre mais que la lettre est contenue dans la grille
                    
                    # Storer les x et y dans une liste pour les comparer et eviter de reprendre une meme lettre?
                    
                    x = row.index(letter)
                    y = grille.index(row)
                    
                    # cas x-1 y
                    a = (x == xInitial - 1 and y == yInitial)
                    # cas x+1 y
                    b = (x == xInitial + 1 and y == yInitial)
                    #cas x y-1
                    c = (x == xInitial and y == yInitial - 1)
                    #cas x y+1
                    d = (x == xInitial and y == yInitial + 1)
                    #cas x-1 y-1
                    e = (x == xInitial - 1 and y == yInitial - 1)
                    #cas x+1 y+1
                    f = (x == xInitial + 1 and y == yInitial + 1)
                    #cas x-1 y+1
                    g = (x == xInitial - 1 and y == yInitial + 1)
                    #cas x+1 y-1
                    h = (x == xInitial + 1 and y == yInitial - 1)

                    if (a or b or c or d or e or f or g or h):
                        valide = True
                    else:
                        valide = False
                        return valide

                    xInitial = row.index(letter)
                    yInitial = grille.index(row)

                    break 
            else:
                valide = False
        i += 1
    return valide

def calcul_point(grille, mots):
    total = 0
    
    # je veux pouvoir utiliser cette fonction pour calculer les points dun seul mot aussi!
    if type(mots) == str:
        if est_valide(grille, mots):
            if len(mots) == 3:
                total += 1
            elif len(mots) == 4:
                total += 2
            elif len(mots) == 5:
                total += 3
            elif len(mots) >= 6:
                total += 5
        else:
            total = 'x'

    # lutilisation standard ou on calcule les points de chaque mot dans une liste de mot
    for mot in mots:
        # On calcule les points dun mot seulement sil est valide!
        if est_valide(grille, mot):
            if len(mot) == 3:
                total += 1
            elif len(mot) == 4:
                total += 2
            elif len(mot) == 5:
                total += 3
            elif len(mot) >= 6:
                total += 5
    return total

def demander_nb_joueurs():
    nb_joueurs = input("Entrez le nombre de joueurs: ")
    while not nb_joueurs.isdecimal():
        nb_joueurs = input("Veuillez entrer un nombre de joueurs entier et positif: ")
    return nb_joueurs

def demander_taille():
    taille = input("Entrez la taille de la grille: ")
    while taille not in "456":
        taille = input("Veuillez entrer une taille entiere et positive entre 4 et 6: ")
    return int(taille)

def demander_mot():
    return "test"

# QUESTION: dans le cas où on a plus que 2 joueurs, est-ce que le mot est rejetté si tous les autres joueurs décident de le rejetter, ou lorsqu'un seul joueur décide de le rejetter?
def demander_rejection(mot, index_joueur_actuel):
    compte_rejets = 0
    
    for i, joueur in enumerate(joueurs):

        if i == index_joueur_actuel:
            continue

        numero = joueur["numero"]
        rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")
        while rejet.upper() not in "ON":
            rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")

        # si le rejet est fait lorsqu'un seul joueur rejette
        # if rejet == "O":
        #     mot_rejette = True
        
        # si le rejet est fait lorsque tous les joueurs rejettent
        if rejet == "O":
            compte_rejets += 1
    
    # selon la méthode de rejection dans QUESTION 
    # s'il y a rejection: on ajoute le mot dans une liste
    # on pourra ensuite utiliser cette liste pour déterminer quels sont les mots rejettés et afficher en conséquence   
    if compte_rejets >= len(joueurs) - 1:
        mots_rejettes.append(mot)

def demander_poursuivre():
    return False

def jouer():
    taille = demander_taille()
    grille = generer_grille(taille)
    nb_joueurs = demander_nb_joueurs()
    joueurs = generer_joueurs(nb_joueurs)
    joueurs_inactifs = []
    partie_en_cours = True

    while partie_en_cours:
        for i, joueur in enumerate(joueurs):
            if joueur not in joueurs_inactifs:  
                mot_actuel = demander_mot()
            demander_rejection(mot_actuel, i)
            demander_poursuivre()
            if not demander_poursuivre() or len(joueur["mots"]) >= 10:
                joueurs_inactifs.append(joueur)
            if len(joueurs_inactifs) >= len(joueurs):
                partie_en_cours = False
                break
    return

def test():
    # check generer_grille()
    # check est_valide()
    # check calcul_point()
    return

def test_generer_grille():
    generer_grille(0)
    # print(grille)
    # print(listeDesChoisis)
    # for i in range(taille):
    #     for j in range(taille):
    #         assert grille[i][j] in listeDesChoisis[i][j], f"la lettre a la pos ({i}, {j}) nest pas contenue dans le de {i+1}"

# Déclaration du code principal et Affichage

#grille = generer_grille(4)
#joueurs = generer_joueurs(2)
#afficher_grille(grille)
#afficher_pointage(grille, joueurs)
jouer()
#print(joueurs)
#################################################################################
# Tests (optionnel)

test()