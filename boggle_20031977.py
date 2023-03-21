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
    25: 'EDUFHK',
    26: 'POATRI',
    27: 'ACBHOG',
    28: 'MVURFN',
    29: 'BETUZC',
    30: 'IOTFAB',
    31: 'JKXBNO',
    32: 'QLPACE',
    33: 'ZBNRWE',
    34: 'DFGPSA',
    35: 'GOILKE',
    36: 'HEVRYA'
}

# Déclaration des fonctions internes et calculs 
# avec commentaires détaillés nécessaires seulement (optionnel)
def generer_grille(taille):

    # Dans le cas où la gestion d'input du user n'est pas assez pour garantir une taille de type valide et qui fonctionne avec le nombre de dés disponibles, on retourne None, None.

    if (type(taille) != int):
        grille = None
        faces_choisies = None
        return grille, faces_choisies

    if taille**2 > len(des):
        grille = None
        faces_choisies = None
        return grille, faces_choisies
    
    grille = [["" for _ in range(taille)] for _ in range(taille)]
    des_choisis = []
    faces_choisies = []
    
    # Pour empêcher de sélectionner un même dé plus d'une fois.

    while len(des_choisis) < taille**2:
        de_random = des[random.randint(1, taille**2)]
        if de_random not in des_choisis:
            des_choisis.append(de_random)
            faces_choisies.append(de_random[random.randint(0, 5)])

    # Construction de la grille à partir d'une liste de faces choisies selon des dés uniques.

    for ligne in range(taille):
        for colonne in range(taille):
            grille[ligne][colonne] = faces_choisies[ligne*4+colonne]
    
    return grille, faces_choisies

def generer_joueurs(nb_joueurs):
    joueurs = []
    
    # Chaque joueur est généré avec ses attributs: numéro, mots, mots rejettés et points totaux par manche.
    
    for joueur in range(int(nb_joueurs)):
        joueur_actuel = {
            "numero" : joueur + 1,
            "mots" : [], 
            "mots_rejettes" : [], 
            "points_totaux" : []
        }
        joueurs.append(joueur_actuel)
    
    return joueurs

def afficher_grille(grille):
    for ligne in grille:
        print('-' * (len(grille) * 4) + '-') # En comptant les '-' avec taille 4, 5 et 6, on trouve le pattern '-'*(taille*4) + '-'.
        print('|', end=' ')                  # '| ' avant chaque lettre.
        for lettre in ligne:
            print(lettre + ' |', end=' ')    # ' |' après chaque lettre.
        print()                              # Newline après chaque ligne.
    print('-' * (len(grille) * 4) + '-')     # Dernière ligne remplie de '-'.

def afficher_pointage_manche(grille, joueurs):   
    longueur_base = 29      # Nombre de caractères total de base dans l'exemple.
    longueur_reste = 18     # Nombre de caractères de la partie incluant seulement ce qu'il se trouve à la droite du pointage. 
    
    for joueur in joueurs:
        numero_joueur = joueur["numero"]
        print(f"JOUEUR {numero_joueur}")
        
        # Pour que l'affichage s'ajuste en fonction du mot le plus long, on fait varier la longueur totale selon le mot le plus long.

        if len(joueur["mots"]) == 0:
            longueur_mot_plus_long = 0
        else:
            longueur_mot_plus_long = len(max(joueur["mots"], key=len))
        longueur_totale = longueur_mot_plus_long + longueur_reste
        
        if longueur_totale > longueur_base:
            print('-'*longueur_totale)
        else:
            print('-'*longueur_base)

            for mot in joueur["mots"]:
                print('- ', end='')

                points = calcul_point(grille, mot)

                if est_valide(grille, mot):
                    mention = ""
                else:
                    points = "x"
                    mention = " -- ILLEGAL "

                if mot in joueur["mots_rejettes"]:
                    points = "x"
                    mention = " -- REJETE "
                elif mot not in joueur["mots_rejettes"] and est_valide(grille, mot):
                    mention = ""

                # Ajustement du nombre d'espaces selon le mot (on fait en sorte que c'est le mot le plus long qui dicte la longueur de l'affichage)

                if len(mot) == longueur_mot_plus_long:
                    print(mot + ' ' + f'({points})' + f'{mention}')
                else:
                    print(mot + ' ' + ' '*(longueur_mot_plus_long - len(mot)) + f'({points})' + f'{mention}')

        if longueur_totale > longueur_base:
            print('='*longueur_totale)
        else:
            print('='*longueur_base)
        
        total = calcul_point(grille, joueur["mots"])
        print(f"TOTAL: {total}")
        print()

def afficher_pointage_fin(joueurs):
    totaux = []
    egalites = []
    
    # Calcul du total des points accumulés à chaque manche seulement à la fin de la partie.
    
    for joueur in joueurs:
        numero_joueur_actuel = joueur["numero"]
        total_joueur_actuel = 0
        
        for t, total in enumerate(joueur["points_totaux"]):
            total_joueur_actuel += joueur["points_totaux"][t]
        
        totaux.append(total_joueur_actuel)
        
        print(f"JOUEUR {numero_joueur_actuel} a {total_joueur_actuel} points.")
    
    # Annonce le vainceur ou l'égalité entre joueurs s'il y a lieu.
    
    for t, total in enumerate(totaux):
        if total == max(totaux):
            egalites.append(total)
    
    if len(egalites) > 1:
        print("JOUEUR ", end="")
        for e, egalite in enumerate(egalites):
            if e+1 != len(egalites):
                print(f"{e+1}, ", end="")
            else:
                print(f"{e+1} ", end="")
        print(f"sont à égalité avec {egalite} points!")
    
    else:
        numero_joueur_gagnant = totaux.index(max(totaux)) + 1
        print(f"JOUEUR {numero_joueur_gagnant} a gagné!")

def est_valide(grille, mot):
    if type(mot) != str or mot == "":           # Caractère vide ou tout autre type que str donne 0 point.
        return False
    
    # On commence par vérifier si la première lettre du mot entré est contenue dans la grille.
    
    for x, ligne in enumerate(grille):
        for y, lettre in enumerate(ligne):
            
            positions_utilisees = []
            
            # On commence par vérifier si la première lettre du mot entré est contenue dans la grille.

            if lettre == mot[0]:
                dernier_x, dernier_y = x, y
                positions_utilisees.append((dernier_x, dernier_y))
                
                # Une fois trouvée, on note sa position puis on cherche un chemin vers les autres lettres du mot à partir de chacune des instances de la première lettre dans la grille.

                for i in range(1, len(mot)):
                    valide = False
                    
                    for mouvement_x in [-1, 0, 1]:                  # On teste toutes les combinaisons de mouvement possible.
                        for mouvement_y in [-1, 0, 1]:              
                            nouveau_x = dernier_x + mouvement_x
                            nouveau_y = dernier_y + mouvement_y
                            
                            # On s'assure qu'on reste dans la grille, que la lettre correspond et qu'elle n'est pas déjà utilisée.

                            if (nouveau_x >= 0 and nouveau_x < len(grille) 
                                and nouveau_y >= 0 and nouveau_y < len(ligne) 
                                and grille[nouveau_x][nouveau_y] == mot[i] 
                                and (nouveau_x, nouveau_y) not in positions_utilisees):
                                
                                dernier_x, dernier_y = nouveau_x, nouveau_y
                                positions_utilisees.append((nouveau_x, nouveau_y))
                                valide = True
                                break
                        
                        if valide:       
                            break           # On arrête de tester les combinaisons de mouvement une fois qu'on a un chemin valide vers la prochaine lettre.
                    
                    if not valide:
                        break               # Deux options ici:
                                            # 1. Toutes les combinaisons de mouvement ont été épuisées sans succès, donc on arrête pour que False soit retourné un peu plus bas.
                                            # 2. Un chemin valide a été trouvé, donc on sort naturellement de la loop (sans le break) pour retourner True juste après.
                
                if valide:
                    return True

    return False

def calcul_point(grille, mots):
    total = 0
    
    if len(grille) == 4:
        
        # Cette partie sert à rendre la fonction utile pour un seul mot (et donc ne pas se retrouver à passer chaque lettre du mot dans un for loop).
        
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

        # Partie standard de la fonction qui sert à traiter des listes de mots.
        
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

def ajouter_points_totaux(grille, joueurs):
    for joueur in joueurs:
        points_totaux = 0
        for mot in joueur["mots"]:
            points_totaux += calcul_point(grille, mot)
        joueur["points_totaux"].append(points_totaux)

def demander_nb_joueurs():
    nb_joueurs = input("Entrez le nombre de joueurs: ")
    
    while not nb_joueurs.isdecimal():
        nb_joueurs = input("Veuillez entrer un nombre de joueurs entier et positif: ")
    
    return nb_joueurs

def demander_taille():
    taille = input("Entrez la taille de la grille: ")
    
    while taille not in "456" or taille == "":
        taille = input("Veuillez entrer une taille entiere et positive entre 4 et 6: ")
    
    return int(taille)

def demander_mot(joueur):
    numero_joueur = joueur["numero"]
    mot = input(f"JOUEUR {numero_joueur} - Entrez votre mot: ")
    
    while not mot.isalpha():
        mot = input(f"JOUEUR {numero_joueur} - Veuillez entrer un mot contenant seulement des lettres de l'alphabet: ")
    
    return mot

def demander_rejection(grille, mot, joueur_, joueurs):
    compte_rejets = 0

    for joueur in joueurs:

        if joueur["numero"] == joueur_["numero"]:
            continue

        if est_valide(grille, mot):                                                 # La mention rejet est possible seulement lorsque le mot n'est pas illégal.
            numero = joueur["numero"]
            rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")
            
            while rejet.upper() not in "ON" or rejet.upper() == "":
                rejet = input(f"JOUEUR {numero} - Rejetter le mot {mot}? [O/N]: ")

            if rejet.upper() == "O":                                                # La mention rejet sera attribuée lorsque tous les autres joueurs rejettent le mot (utile pour des parties de 3 joueurs et +).
                compte_rejets += 1
    
    if compte_rejets >= len(joueurs) - 1:
        joueurs[joueur_["numero"]]["mots_rejettes"].append(mot)
        return True
    
    return False

def demander_poursuivre(joueur):
    numero_joueur = joueur["numero"]
    poursuivre = input(f"JOUEUR {numero_joueur} - Voulez-vous poursuivre? [O/N]: ")
    
    while poursuivre.upper() not in "ON" or poursuivre.upper() == "":
        poursuivre = input(f"JOUEUR {numero_joueur} - Voulez-vous poursuivre? [O/N]: ")
    
    if poursuivre.upper() == "O":
        poursuivre_bool = True
    
    elif poursuivre.upper() == "N":
        poursuivre_bool = False
    
    return poursuivre_bool

def demander_nb_manches():
    nb_manches = input("Entrez le nombre de manches: ")
    
    while not nb_manches.isdecimal():
        nb_manches = input("Veuillez entrer un nombre de manches entier et positif: ")
    
    return int(nb_manches)

def demander_nouvelle_partie():
    nouvelle_partie = input("Voulez-vous jouer une nouvelle partie? [O/N]: ")
    
    while nouvelle_partie.upper() not in "ON" or nouvelle_partie.upper() == "":  
        nouvelle_partie = input("Voulez-vous jouer une nouvelle partie? [O/N]: ")
    
    if nouvelle_partie.upper() == "N":
        return False
    
    elif nouvelle_partie.upper() == "O":
        return True

def jouer_tours(grille, joueurs):
    manche_en_cours = True

    joueurs_inactifs = []

    for joueur in joueurs:  
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

def jouer_manches():
    taille = demander_taille()  
    grille, faces_choisies = generer_grille(taille)             # faces_choisies est seulement déclaré pour que seulement la valeur de retour grille soit assignée à grille 
    joueurs = generer_joueurs(demander_nb_joueurs())            # (puisque generer_grille(taille) retourne une grille et une liste des faces de dés choisies).
    nb_manches = demander_nb_manches()
    
    afficher_grille(grille)
    
    for manche in range(nb_manches):

        jouer_tours(grille, joueurs)
        ajouter_points_totaux(grille, joueurs)
        afficher_pointage_manche(grille, joueurs)
        print("Manche terminée!")
        
        if manche < nb_manches - 1:                             # Pas besoin de générer une nouvelle grille si c'est la dernière manche.
            grille, faces_choisies = generer_grille(taille)     # Même principe que le faces_choisies ci-haut.

        afficher_grille(grille)

    afficher_pointage_fin(joueurs)
    print("Partie terminée!")

def jouer():
    partie_en_cours = True   

    while partie_en_cours: 

        jouer_manches()
        
        if not demander_nouvelle_partie():
            partie_en_cours = False

def comparer_matrices(matrice_1, matrice_2):
    if len(matrice_1) != len(matrice_2):
        return False
    
    for i in range(len(matrice_1)):
        if len(matrice_1[i]) != len(matrice_2[i]):
            return False
        for j in range(len(matrice_1[i])):
            if matrice_1[i][j] != matrice_2[i][j]:
                return False
    
    return True

def test():
    test_generer_grille()
    test_est_valide()
    test_calcul_point()

def test_generer_grille():
    tailles = [4, 5, 6]

    for taille in tailles:
        grille_1, faces_choisies_1 = generer_grille(taille)
        grille_2, faces_choisies_2 = generer_grille(taille)

        assert comparer_matrices(grille_1, grille_2) == False, "Échec: Deux grilles générées devraient pratiquement toujours être différentes."

        assert len(grille_1) == taille, "Échec: len(grille) == taille."
        for i, ligne in enumerate(grille_1):
            assert len(ligne) == taille, "Échec: len(ligne) == taille."
            for j, lettre in enumerate(ligne):
                assert lettre in faces_choisies_1[4*i + j], "Échec: lettre in faces_choisies[4*i + j]."
    
    assert generer_grille(7) == (None, None), "Échec: taille invalide (valeur trop grande) ne devrait pas générer de grille ou de liste de faces choisies."
    assert generer_grille('GG') == (None, None), "Échec: taille invalide (type) ne devrait pas générer de grille ou de liste de faces choisies."
    assert generer_grille(0) == ([], []), "Échec: taille = 0 devrait générer une grille vide et une liste de faces choisies vide."

def test_est_valide():
    grille = [['A', 'B', 'A', 'D'],
              ['E', 'F', 'G', 'H'],
              ['I', 'A', 'K', 'L'],
              ['M', 'N', 'O', 'P']]
    
    assert est_valide(grille, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA') == False, "Échec: mot constitué d'une répétition de même lettre (même position réutilisée)."
    assert est_valide(grille, 3) == False, "Échec: mot de type autre que 'str'"
    assert est_valide(grille, 'Z') == False, "Échec: mot composé de lettres qui ne se trouvent pas dans la grille."
    assert est_valide(grille, '') == False, "Échec: mot vide."
    assert est_valide(grille, 'EGMP') == False, "Échec: mot composé de lettres dans la grille, mais qui ne sont pas adjacents."

    assert est_valide(grille, 'ABA') == True, "Échec: mot horizontal."
    assert est_valide(grille, 'AFK') == True, "Échec: mot diagonal."
    assert est_valide(grille, 'AEI') == True, "Échec: mot vertical."
    assert est_valide(grille, 'AFBEIA') == True, "Échec: mot combiné (horizontal + vertical + diagonal)."
    assert est_valide(grille, 'AKL') == True, "Échec: mot avec première lettre présente plusieurs fois dans la grille et qui n'est pas formé à partir de la première instance de la dite première lettre."

def test_calcul_point():
    grille = [['A', 'B', 'C', 'D'],
              ['E', 'F', 'G', 'H'],
              ['I', 'J', 'K', 'L'],
              ['M', 'N', 'O', 'P']]
    
    liste_mots = ['ABCD', '', 'AB', 'AFBE', 23]

    assert calcul_point(grille, '') == 0, "Échec: calcul_point(grille, 'A') == 0."
    assert calcul_point(grille, 'ACJP') == 0, "Échec: calcul_point(grille, 'ACJP'), où 'ACJP' est un mot invalide."
    assert calcul_point(grille, 'ABCD') == 2, "Échec: calcul_point(grille, 'ABCD'), où 'ABCD' est un mot valide."
    assert calcul_point(grille, 23) == 0, "Échec: calcul_point(grille, 23)."
    assert calcul_point(grille, liste_mots) == 4, "Échec: calcul_point(grille, liste_mots)."

# Déclaration du code principal et Affichage
jouer()

#################################################################################
# Tests (optionnel)
test()