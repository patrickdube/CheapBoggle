###############################################################################
## Programme qui simule une version simplifiee du jeu Boggle.
###############################################################################
## Auteurs: Patrick Dube, Johann Sourou
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
liste_totaux = []
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

# DONE
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

# DONE
def generer_joueurs(nb_joueurs):
    for joueur in range(int(nb_joueurs)):
        liste_mots_joueurs.append([])
        joueur_actuel = {
            "numero" : joueur + 1,
            "mots" : liste_mots_joueurs[joueur]
        }
        joueurs.append(joueur_actuel)
    return joueurs

# DONE
# Pas besoin de grille en param puisque grille est globale et generer_grille() la remplie avant cet appel
def afficher_grille():
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

# DONE
def afficher_pointage(joueurs):   
    longueur_base = 29 
    longueur_reste = 18

    # IDEA: faire un for loop pour passer tous les joueurs 
    # PAR CONTRE: il faut aussi un affichage pour un seul joueur
    
    for joueur in joueurs:
        numero_joueur = joueur["numero"]
        mots_joueurs_actuel = joueur["mots"]
        longueur_mot_plus_long = len(max(mots_joueurs_actuel, key=len))
        longueur_totale = longueur_mot_plus_long + longueur_reste

        print(f"JOUEUR {numero_joueur}")
   
        if longueur_totale > longueur_base:
            print('-'*longueur_totale)
        else:
            print('-'*longueur_base)

            for mot in mots_joueurs_actuel:
                print('- ', end='')

                # mention ILLEGAL
                if est_valide(mot):
                    mention = ""
                else:
                    mention = " -- ILLEGAL "

                # mention REJETE
                if mot in mots_rejettes:
                    mention = " -- REJETE "
                else:
                    mention = ""

                # ajustement de laffichage, centrer en un point fixe
                if len(mot) == longueur_mot_plus_long:
                    print(mot + ' ' + f'({calcul_point(mot)})' + f'{mention}')
                else:
                    print(mot + ' ' + ' '*(longueur_mot_plus_long - len(mot)) + f'({calcul_point(mot)})' + f'{mention}')

        #AFFICHAGE ========
        if longueur_totale > longueur_base:
            print('='*longueur_totale)
        else:
            print('='*longueur_base)

        #AFFICHAGE TOTAL
        print(f"TOTAL: {calcul_point(mots_joueurs_actuel)}")

        print()

# NOT DONE
# TODO: verifier si le mot nest pas deja trouve par un autre joueur -- en faire une autre fonction et lappeler dans jouer()?   
def est_valide(mot):
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
                    a = (x == xInitial - 1 and y == yInitial) and (x < len(grille) - 1)
                    # cas x+1 y
                    b = (x == xInitial + 1 and y == yInitial) and (x > 0)
                    #cas x y-1
                    c = (x == xInitial and y == yInitial - 1) and (y < len(grille) - 1)
                    #cas x y+1
                    d = (x == xInitial and y == yInitial + 1) and (y > 0)
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

# DONE
def calcul_point(mots):
    total = 0
    
    # je veux pouvoir utiliser cette fonction pour calculer les points dun seul mot aussi!
    if type(mots) == str:
        if est_valide(mots):
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
        if est_valide(mot):
            if len(mot) == 3:
                total += 1
            elif len(mot) == 4:
                total += 2
            elif len(mot) == 5:
                total += 3
            elif len(mot) >= 6:
                total += 5
    return total

# DONE
def demander_nb_joueurs():
    nb_joueurs = input("Entrez le nombre de joueurs: ")
    while not nb_joueurs.isdecimal():
        nb_joueurs = input("Veuillez entrer un nombre de joueurs entier et positif: ")
    return nb_joueurs

# DONE
def demander_taille():
    taille = input("Entrez la taille de la grille: ")
    while taille not in "456":
        taille = input("Veuillez entrer une taille entiere et positive entre 4 et 6: ")
    return int(taille)

# NOT DONE
def demander_mot():
    return "test"

# DONE
def demander_rejection(mot, index_joueur_actuel):
    compte_rejets = 0
    
    for i, joueur in enumerate(joueurs):

        if i == index_joueur_actuel:
            continue

        if est_valide(mot): # la mention rejet est possible seulement lorsque le mot est valide, mais que les autres joueurs rejettent le mot
            numero = joueur["numero"]
            rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")
            while rejet.upper() not in "ON":
                rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")

            # si le rejet est fait lorsqu'un seul joueur rejette
            # if rejet == "O":
            #     mots_rejettes.append(mot)
            #     break

            # si le rejet est fait lorsque tous les joueurs rejettent
            if rejet == "O":
                compte_rejets += 1
    
    # s'il y a rejection: on ajoute le mot dans une liste
    # on pourra ensuite utiliser cette liste pour déterminer quels sont les mots rejettés et afficher en conséquence   
    if compte_rejets >= len(joueurs) - 1:
        mots_rejettes.append(mot)

# DONE
def demander_poursuivre(index_joueur_actuel):
    poursuivre = input(f"JOUEUR {index_joueur_actuel} - Voulez-vous poursuivre? [O/N]: ")
    while poursuivre.upper() not in "ON":
        poursuivre = input(f"JOUEUR {index_joueur_actuel} - Voulez-vous poursuivre? [O/N]: ")
    if poursuivre.upper() == "O":
        poursuivre_bool = True
    else:
        poursuivre_bool = False
    return poursuivre_bool

# DONE
def demander_nb_manches():
    nb_manches = input("Entrez le nombre de manches: ")
    while not nb_manches.isdecimal():
        nb_manches = input("Veuillez entrer un nombre de manches entier et positif: ")
    return int(nb_manches)

# DONE
def jouer_tours():
    joueurs_inactifs = []
    manche_en_cours = True

    while manche_en_cours:
        
        for i, joueur in enumerate(joueurs):
            
            if joueur not in joueurs_inactifs:  
                mot_actuel = demander_mot()

            if not demander_rejection(mot_actuel, i):
                joueur["mots"].append(mot_actuel)
            
            if not demander_poursuivre(i+1) or len(joueur["mots"]) >= 10:
                joueurs_inactifs.append(joueur)
            
            if len(joueurs_inactifs) >= len(joueurs):
                manche_en_cours = False
                break
        
        print("Tour terminé!")

# DONE
def jouer_manches(nb_manches, taille):
    for manche in range(nb_manches):
        
        # on reinitie les listes de mots des joueurs a chaque debut de manche
        for joueur in joueurs:  # on utilise la liste de joueurs globale, remplie par generer_joueurs() avant lappel de cette fonction
            joueur["mots"] = []
        
        jouer_tours()

        totaux = []
        for joueur in joueurs:
            numero = joueur["numero"]
            total = calcul_point(joueur["mots"])
            print(f"Points du joueur {numero}: {total}")
            totaux.append(total)                            # liste ordonnee des totaux de chaque joueur
        liste_totaux.append(totaux)                         # liste contenant les listes de totaux de chaque joueur pour chaque manche

        print("Manche terminée!")
        
        if manche < nb_manches: # pas besoin de generer une grille si cest la derniere manche
            global grille
            grille = []
            generer_grille(taille)

            afficher_grille()

# DONE
def jouer():
    taille = demander_taille()
    generer_grille(taille)
    
    nb_joueurs = demander_nb_joueurs()
    generer_joueurs(nb_joueurs)
    
    nb_manches = demander_nb_manches()
    
    afficher_grille()

    jouer_manches(nb_manches, taille)

    afficher_pointage(joueurs)
    
    print("Partie terminée!")

# NOT DONE
def test():
    # check generer_grille()
    # check est_valide()
    # check calcul_point()
    return

# NOT DONE
def test_generer_grille():
    generer_grille(0)
    # print(grille)
    # print(listeDesChoisis)
    # for i in range(taille):
    #     for j in range(taille):
    #         assert grille[i][j] in listeDesChoisis[i][j], f"la lettre a la pos ({i}, {j}) nest pas contenue dans le de {i+1}"
    # - Pour toute taille valide, la fonction me retourne un tableau à 2 dimensions où chaque sous-tableau est de même longueur et est composée de valeurs valides (dés) 
    # - Pour deux appels successifs, la fonction ne génère pas la même grille
    # - Pour toute taille non valide, la fonction me retourne un tableau vide (ou autre comportement)
# NOT DONE
def test_est_valide():
    pass

# NOT DONE
def test_calcul_point():
    pass

# Déclaration du code principal et Affichage
jouer()

#################################################################################
# Tests (optionnel)
test()