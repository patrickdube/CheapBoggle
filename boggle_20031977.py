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
    grille = [["" for _ in range(taille)] for _ in range(taille)]
    
    # empeche de prendre un de plus dune fois
    des_choisis = []
    faces_choisies = []
    while len(des_choisis) < taille**2:
        de_random = des[random.randint(1, taille**2)]
        if de_random not in des_choisis:
            des_choisis.append(de_random)
            faces_choisies.append(de_random[random.randint(0, 5)])

    # construction de la grille a partir dune liste de faces choisies provenant de des aleatoires choisis
    for ligne in range(taille):
        for colonne in range(taille):
            grille[ligne][colonne] = faces_choisies[ligne*4+colonne]
    
    return grille

# DONE
def generer_joueurs(nb_joueurs):
    joueurs = []
    
    for joueur in range(int(nb_joueurs)):
        joueur_actuel = {
            "numero" : joueur + 1,
            "mots" : [], 
            "mots_rejettes" : [], 
            "points_totaux" : [] # totaux par manche
        }
        joueurs.append(joueur_actuel)
    
    return joueurs

# DONE
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

# DONE
def afficher_pointage_manche(grille, joueurs):   
    longueur_base = 29 
    longueur_reste = 18
    
    for joueur in joueurs:
        numero_joueur = joueur["numero"]
        if len(joueur["mots"]) == 0:
            longueur_mot_plus_long = 0
        else:
            longueur_mot_plus_long = len(max(joueur["mots"], key=len))
        longueur_totale = longueur_mot_plus_long + longueur_reste

        print(f"JOUEUR {numero_joueur}")
   
        if longueur_totale > longueur_base:
            print('-'*longueur_totale)
        else:
            print('-'*longueur_base)

            for mot in joueur["mots"]:
                print('- ', end='')

                points = calcul_point(grille, mot)

                # mention ILLEGAL
                if est_valide(grille, mot):
                    mention = ""
                else:
                    points = "x"
                    mention = " -- ILLEGAL "

                # mention REJETE
                if mot in joueur["mots_rejettes"]:
                    points = "x"
                    mention = " -- REJETE "
                elif mot not in joueur["mots_rejettes"] and est_valide(grille, mot):
                    mention = ""

                # ajustement de laffichage, centrer en un point fixe
                if len(mot) == longueur_mot_plus_long:
                    print(mot + ' ' + f'({points})' + f'{mention}')
                else:
                    print(mot + ' ' + ' '*(longueur_mot_plus_long - len(mot)) + f'({points})' + f'{mention}')

        #AFFICHAGE ========
        if longueur_totale > longueur_base:
            print('='*longueur_totale)
        else:
            print('='*longueur_base)
        
        total = calcul_point(grille, joueur["mots"])
        print(f"TOTAL: {total}")
        print()

# NOT DONE
def afficher_pointage_fin(joueurs):
    totaux = []
    
    for joueur in joueurs:
        numero_joueur_actuel = joueur["numero"]
        total_joueur_actuel = 0
        
        for t, total in enumerate(joueur["points_totaux"]):
            total_joueur_actuel += joueur["points_totaux"][t]
        
        totaux.append(total_joueur_actuel)
        
        print(f"JOUEUR {numero_joueur_actuel} a {total_joueur_actuel} points.")
    
    # il faut couvrir le cas ou des joueurs sont a egalite
    numero_joueur_gagnant = totaux.index(max(totaux)) + 1
    print(f"JOUEUR {numero_joueur_gagnant} a gagné!")

# NOT DONE
# TODO: verifier si le mot nest pas deja trouve par un autre joueur -- en faire une autre fonction et lappeler dans jouer()?   
def est_valide(grille, mot):
    # Check that each letter is present in the grid.
    previous_positions = []
    # Check all possible starting positions for the first letter.
    for x, row in enumerate(grille):
        for y, letter in enumerate(row):
            if letter == mot[0]:
                # Check if adjacent letters in the word are adjacent in the grid.
                prev_x, prev_y = x, y
                previous_positions.append((prev_x, prev_y))
                for i in range(1, len(mot)):
                    found = False
                    for x_offset in [-1, 0, 1]:
                        for y_offset in [-1, 0, 1]:
                            new_x = prev_x + x_offset
                            new_y = prev_y + y_offset
                            if (new_x >= 0 and new_x < len(grille) and new_y >= 0 and new_y < len(row) and grille[new_x][new_y] == mot[i]) and (new_x, new_y) not in previous_positions:
                                prev_x, prev_y = new_x, new_y
                                previous_positions.append((new_x, new_y))
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        break
                if found:
                    return True

    return False

# DONE
def calcul_point(grille, mots):
    total = 0
    if len(grille) == 4:
        # je veux pouvoir utiliser cette fonction pour calculer les points dun seul mot aussi (qui ne sont pas contenu dans une liste)!
        if type(mots) == str:
            if est_valide(grille, mots):
                if len(mots) == 3:
                    total += 1
                elif len(mots) == 4:
                    total += 2
                elif len(mots) == 5:
                    total += 3
                elif len(mots) == 6:
                    total += 5
                elif len(mots) == 7:
                    total += 8
                elif len(mots) >= 8:
                    total += 10

        if type(mots) == list: # pour eviter de parser un str comme si cetait une liste et donc eviter de doubler les points
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
                    elif len(mot) == 6:
                        total += 5
                    elif len(mot) == 7:
                        total += 8
                    elif len(mot) >= 8:
                        total += 10
    
    elif len(grille) == 5:
        if type(mots) == str:
            if est_valide(grille, mots):
                if len(mots) == 3:
                    total += 1
                elif len(mots) == 4:
                    total += 2
                elif len(mots) == 5:
                    total += 3
                elif len(mots) == 6:
                    total += 4
                elif len(mots) == 7:
                    total += 6
                elif len(mots) >= 8:
                    total += 10

        if type(mots) == list: 
            for mot in mots:
                if est_valide(grille, mot):
                    if len(mot) == 3:
                        total += 1
                    elif len(mot) == 4:
                        total += 2
                    elif len(mot) == 5:
                        total += 3
                    elif len(mot) == 6:
                        total += 4
                    elif len(mot) == 7:
                        total += 6
                    elif len(mot) >= 8:
                        total += 10

    elif len(grille) == 6:
        if type(mots) == str:
            if est_valide(grille, mots):
                if len(mots) == 3:
                    total += 1
                elif len(mots) == 4:
                    total += 2
                elif len(mots) == 5:
                    total += 3
                elif len(mots) == 6:
                    total += 5
                elif len(mots) == 7:
                    total += 7
                elif len(mots) == 8:
                    total += 10
                elif len(mots) >= 9:
                    total += 12

        if type(mots) == list: 
            for mot in mots:
                if est_valide(grille, mot):
                    if len(mot) == 3:
                        total += 1
                    elif len(mot) == 4:
                        total += 2
                    elif len(mot) == 5:
                        total += 3
                    elif len(mot) == 6:
                        total += 5
                    elif len(mot) == 7:
                        total += 7
                    elif len(mot) == 8:
                        total += 10
                    elif len(mot) >= 9:
                        total += 12
    return total

# DONE
def ajouter_points_totaux(grille, joueurs):
    for joueur in joueurs:
        points_totaux = 0
        for mot in joueur["mots"]:
            points_totaux += calcul_point(grille, mot)
        joueur["points_totaux"].append(points_totaux)

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

# DONE
def demander_mot(joueur):
    numero_joueur = joueur["numero"]
    mot = input(f"JOUEUR {numero_joueur} - Entrez votre mot: ")
    while not mot.isalpha():
        mot = input(f"JOUEUR {numero_joueur} - Veuillez entrer un mot contenant seulement des lettres de l'alphabet: ")
    
    return mot

# DONE 
def demander_rejection(grille, mot, joueur_, joueurs):
    compte_rejets = 0

    for joueur in joueurs:

        if joueur["numero"] == joueur_["numero"]:
            continue

        if est_valide(grille, mot): # la mention rejet est possible seulement lorsque le mot est valide, mais que les autres joueurs rejettent le mot
            numero = joueur["numero"]
            rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")
            while rejet.upper() not in "ON":
                rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")

            # si le rejet est fait lorsqu'un seul joueur rejette
            # if rejet == "O":
            #     mots_rejettes.append(mot)
            #     break

            # si le rejet est fait lorsque tous les joueurs rejettent
            if rejet.upper() == "O":
                compte_rejets += 1
    
    if compte_rejets >= len(joueurs) - 1:
        joueurs[joueur_["numero"]]["mots_rejettes"].append(mot)
        return True
    
    return False

# DONE
def demander_poursuivre(joueur):
    numero_joueur = joueur["numero"]
    poursuivre = input(f"JOUEUR {numero_joueur} - Voulez-vous poursuivre? [O/N]: ")
    while poursuivre.upper() not in "ON":
        poursuivre = input(f"JOUEUR {numero_joueur} - Voulez-vous poursuivre? [O/N]: ")
    
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
def demander_nouvelle_partie():
    nouvelle_partie = input("Voulez-vous jouer une nouvelle partie? [O/N]: ")
    while nouvelle_partie.upper() not in "ON":  
        nouvelle_partie = input("Voulez-vous jouer une nouvelle partie? [O/N]: ")
    if nouvelle_partie.upper() == "N":
        return False
    return True

# DONE
def jouer_tours(grille, joueurs):
    manche_en_cours = True

    # les joueurs qui ont decide darreter de jouer last manche peuvent rejouer
    joueurs_inactifs = []

    # on reinitie les listes de mots des joueurs a chaque debut de manche
    for joueur in joueurs:  # on utilise la liste de joueurs globale, remplie par generer_joueurs() avant lappel de cette fonction
        joueur["mots"] = []

    while manche_en_cours:
        
        for joueur in joueurs:
            
            if joueur not in joueurs_inactifs:  
                mot_actuel = demander_mot(joueur)

            if not demander_rejection(grille, mot_actuel, joueur, joueurs):
                joueur["mots"].append(mot_actuel)
            
            if not demander_poursuivre(joueur) or len(joueur["mots"]) >= 10:
                joueurs_inactifs.append(joueur)
            
            if len(joueurs_inactifs) >= len(joueurs):
                manche_en_cours = False
                break
        
        print("Tour terminé!")

# DONE
def jouer_manches():
    taille = demander_taille()  
    grille = generer_grille(taille)
    joueurs = generer_joueurs(demander_nb_joueurs())
    nb_manches = demander_nb_manches()
    
    afficher_grille(grille)
    
    for manche in range(nb_manches):
        
        # pas besoin de passer joueurs inactifs sil est declaree au debut de jouer_tours ??? a voir
        jouer_tours(grille, joueurs)
        ajouter_points_totaux(grille, joueurs)
        afficher_pointage_manche(grille, joueurs) # on veut afficher les points de la derniere manche, et non pas celle a venir! donbc important de faire cet appel avant le nouvel appel de generer_grille
        print("Manche terminée!")
        
        if manche < nb_manches - 1: # pas besoin de generer une grille si cest la derniere manche
            grille = generer_grille(taille) 

        afficher_grille(grille)

    afficher_pointage_fin(joueurs)
    print("Partie terminée!")

# DONE
def jouer():
    partie_en_cours = True   

    while partie_en_cours: 
    
        jouer_manches()

        if not demander_nouvelle_partie():
            partie_en_cours = False

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