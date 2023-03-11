###############################################################################
## Programme qui simule une version simplifiee du jeu Boggle.
###############################################################################
## Auteur: Patrick Dube
## Copyright: Copyright 2023, boggle_20031977.py
## Version: 1.0.0
## Date: 08/03/23
## Email: patrick.dube.3@umontreal.ca
###############################################################################

# IDEAS
# - add player struct to store player related attributes and expand to more players?
# - make it so the grid can be bigger
# - to track diags in a 4x4: 
#        middle diag: grid[0][0], grid[1][1], grid[2][2], grid[3][3]
#        upper+1 diag: grid[0][1], grid[1][2], grid[2][3]
#        upper+2 diag: grid[0][2], grid[1][3]
#        upper+3 diag: grid[0][3]
# - track points and save them for a game with multiple sets (add points to the player struct?)
# - more than 2 players (so player struct is a good idea here)

# Déclaration des imports et dépendances
import random

# Déclaration des variables globales, constantes
grilleGeneree = []
# listeDesChoisis = []
# TODO: rajouter 11 des pour un tableau 6x6
des = {1: 'ETUKNO', 
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
       25: 'EDUFHK'}
listeMotsJoueur1 = ['ALLO', 'TEST', 'yo']
listeMotsJoueur2 = ['supe', 'TEST']
listeListeMotsJoueurs = [listeMotsJoueur1, listeMotsJoueur2]
width = 29
xInitial = 0
yInitial = 0

# Déclaration des fonctions internes et calculs 
# avec commentaires détaillés nécessaires seulement (optionnel)

def generer_grille(taille):
    for row in range(taille):
        grilleGeneree.append([])
        # listeDesChoisis est une liste 2D qui contient tous les des choisis par le random.randint()
        # listeDesChoisis.append([])
        for _ in range(taille):
            # taille**2 evite dutiliser un if, car si taille == 4, alors taille**2 == 16 et donc seulement les des 1 a 16 sont pris
            de = des[random.randint(1, taille**2)]
            faceDe = de[random.randint(0, 5)]
            grilleGeneree[row].append(faceDe)
            # listeDesChoisis[i].append(de)
    #grilleGeneree = [['a', 'b', 'c', 'd'],['a', 'e', 'i', 'o'],['p','u','o','b'],['y','r','s','n']]

    return grilleGeneree

def afficher_grille(grille):
    for row in grille:
        # top line de ----------- a chaque new line
        print('-'*(len(grille)*4)+'-')
        # le | manquant du debut de chaque ligne de la premiere colonne puisquon ne fait que mettre un ' |' apres chaque element (il manque donc celui du debut avant chaque premier element de chaque ligne)
        print('|', end=' ')
        for mot in row:
            print(mot + ' |', end=' ')
        print()
    # bottom line de ------------ (vu quon met la top line dans la loop, il va manquer une derniere ligne de -------------)
    print('-'*(len(grille)*4)+'-')

def afficher_pointage(grille, numeroJoueur):   
    listeMotsJoueurActuel = listeListeMotsJoueurs[numeroJoueur - 1]
    longueurMotLePlusLong = len(max(listeMotsJoueurActuel, key=len))
    # pourquoi + 18? Pcq jai compte la longueur du reste des caracteres mis a part le mot, et dans notre cas cest 18 (en incluant la decision la plus longue (' -- ILLEGAL ')
    # TODO: storer le len du restant des caracteres pour eviter de 'hardcoder' une valeur du genre 18
    longueurNecessaire = longueurMotLePlusLong + 18
    
    # AFFICHAGE JOUEUR 1-2-3-4-5-...
    print(f"JOUEUR {numeroJoueur}")
    
    # AFFICHAGE -----------------, width de 29 comme dans lexemple du prof (minimum), plus au besoin
    if longueurNecessaire > width:
        print('-'*longueurNecessaire)
    else:
        print('-'*width)
    
    # AFFICHAGE - MOT       (POINT) -- DECISION
    for mot in listeMotsJoueurActuel:
        print('- ', end='')
        
        # mention ILLEGAL
        if est_valide(grille, mot):
            legalite = ""
        else:
            legalite = " -- ILLEGAL "

        # TODO: implementer la mention -- REJETER
        
        # ajustement de laffichage, centrer en un point fixe
        if len(mot) == longueurMotLePlusLong:
            print(mot + ' ' + f'({calcul_point(grille, mot)})' + f'{legalite}')
        else:
            print(mot + ' ' + ' '*(longueurMotLePlusLong - len(mot)) + f'({calcul_point(grille, mot)})' + f'{legalite}')
    
    #AFFICHAGE ========
    if longueurNecessaire > width:
        print('='*longueurNecessaire)
    else:
        print('='*width)
    
    #AFFICHAGE TOTAL
    print(f"TOTAL: {calcul_point(grille, listeMotsJoueurActuel)}")

# TODO: verifier si le mot nest pas deja trouve par un autre joueur -- en faire une autre fonction et lappeler dans jouer()?   
def est_valide(grille, mot):
    # un mot est valide quand:
    # 1. same column
    # 2. same line
    # 3. adjacent letters, but not necessarily same line or same column (BONUS)
    # 4. le mot nest pas deja touve
    
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

# Fonction qui calcule soit les points dun seul mot, soit les points dune liste de mots
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

def jouer():
    tailleGrille = input("Entrez la taille du jeu (par exemple, taille 6 génère un jeu 6x6): ")
    # nbJoueurs = input("Entrez le nombre de joueurs: ")
    nbManches = input("Entrez le nombre de manches: ")
    # 2. generer la grille
    grilleGeneree = generer_grille(tailleGrille)
    # 3. afficher la grille
    afficher_grille(grilleGeneree)
    # 4. JOUER TOUR
        # 4.1 joueur entre mot (demander si le joueur veut entrer un mot)
        # 4.2 autres joueurs rejettent ou non le mot
        # FIN TOUR quand len(mots) de tous les joueurs == 10 (si len(mots) dun joueur == 10, il ne peut plus entrer de mots jusqua ce que la partie se termine)
        # FIN TOUR quand tous les joueurs choisissent de ne plus entrer de mot
    # 5. Calculer les points de chaque joueur
    # 6. Manche suivante, retour au point 4.
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
grille = generer_grille(4)
afficher_grille(grille)
afficher_pointage(grille, 2)
#################################################################################
# Tests (optionnel)
test()