from library import *
from time import sleep
from random import *

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
    """
    Fonction recevant les coordonnées d'une case du plateau sous la forme d'un couple d'entiers (ligne, colonne) et renvoyant les coordonnées du pixel se trouvant au centre de cette case. Ce calcul prend en compte la taille de chaque case, donnée par la variable globale taille_case.
    """

    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    """
    Fonction qui affiche les pommes aléatoirement, de façon à ce que chaque pommes ne soit pas afficher sur la position du serpent ou sur un obstacle
    """

    while len(pommes) != 1:
        x, y = randint(0,largeur_plateau-1), randint(0,hauteur_plateau-1)
        if not((x,y) in serpent1) and not((x,y) in obstacle) :
            pommes.append((x,y))
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')



def affiche_serpent(serpent,couleur):
    for i in serpent:
        x, y = case_vers_pixel(i)
        cercle(x, y, taille_case/2 + 1,couleur="darkgreen", remplissage="green")


def change_direction1(direction, touche):
    """
    Fonction qui assigne les touches utilisées par le premier joueur pour deplacer le premier serpent
    """

    if touche == 'Up' and direction != (0,1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0,-1):
        # flèche bas pressée
        return (0, 1)
    elif touche == 'Left' and direction != (1,0):
        # flèche gauche pressée
        return (-1, 0)
    elif touche == 'Right' and direction != (-1,0):
        # flèche droite pressée
        return (1, 0)
    else:
        # pas de changement !
        return direction


def change_direction2(direction, touche):
    """
    Fonction qui assigne les touches utilisées par le deuxième joueur pour deplacer le deuxième serpent
    """

    if touche == 'z' and direction != (0,1):
        # touche z pressée
        return (0, -1)
    elif touche == 's' and direction != (0,-1):
        # touche s pressée
        return (0, 1)
    elif touche == 'q' and direction != (1,0):
        # touche q pressée
        return (-1, 0)
    elif touche == 'd'and direction != (-1,0):
        # touche d pressée
        return (1, 0)
    else:
        # pas de changement !
        return direction


def dps_serpent(serpent, x, y, xdir, ydir):
    """
    Fonction qui effectue le mouvement du serpent, il ajoute une case devant la tete dans la direction du mouvement
    """

    if x+xdir < 0 or x+xdir >= largeur_plateau:
        serpent.insert(0, ((largeur_plateau-1)*(-(x+xdir)%largeur_plateau), y+ydir))
    elif y+ydir < 0 or y+ydir >= hauteur_plateau:
        serpent.insert(0, (x+xdir, (hauteur_plateau-1)*(-(y+ydir)%hauteur_plateau)))
    else:
        serpent.insert(0, (x+xdir, y+ydir))


def affiche_obstacle(obstacle,framerate):
    """
    Fonction qui affiche les obstacles sur la zone de jeu
    """

    while len(obstacle) < framerate:
        x, y = randint(0,largeur_plateau-1), randint(0,hauteur_plateau-1)
        if not((x,y) in serpent1) and not((x,y) in pommes) and not((x,y) in obstacle):
            obstacle.append((x,y))

    for i in obstacle:
        x, y = case_vers_pixel(i)
        cercle(x, y, taille_case/2 ,couleur="black", remplissage="black")


def affiche_score(score):
    """
    Fonction qui affiche le score du joueur
    """

    efface_tout()
    texte(taille_case*largeur_plateau/2, taille_case*hauteur_plateau/2, "Score = "+str(score), taille = 70, couleur = "red", ancrage = "center")
    attend_clic_gauche()


# programme principal
if __name__ == "__main__":


    # initialisation du jeu
    direction1 = (0, 0)  # direction initiale du serpent1
    direction2 = (0, 0)  #direction initiale du serpent2
    pommes = [] # liste des coordonnées des cases contenant des pommes
    serpent1 = [(0, 0)] # liste des coordonnées de cases adjacentes décrivant le serpent
    serpent2=[(largeur_plateau-1,hauteur_plateau-1)] # liste des coordonnées de cases adjacentes décrivant le serpent2
    obstacle = [] # liste des coordonnées ou il y a des obstacle
    score = 0
    framerate = 10  # taux de rafraîchissement du jeu en images/s qui augmente a chaque fois que l'on mange une pomme
    cree_fenetre(taille_case * largeur_plateau,taille_case * hauteur_plateau)
    mode_jeu = 0



    # boucle principale
    jouer = True
    while jouer==True:

        #Choix du mode de jeu
        while mode_jeu == 0:
            rectangle(0, 0 ,taille_case*largeur_plateau, taille_case*hauteur_plateau/4, remplissage="black", epaisseur=0)
            rectangle(0, taille_case*hauteur_plateau/4, taille_case*largeur_plateau, taille_case*hauteur_plateau, remplissage="white", epaisseur=0)
            rectangle(0, 2*taille_case*hauteur_plateau/4, taille_case*largeur_plateau, taille_case*hauteur_plateau, remplissage="black", epaisseur=0)
            rectangle(0, 3*taille_case*hauteur_plateau/4, taille_case*largeur_plateau, taille_case*hauteur_plateau, remplissage="white", epaisseur=0)
            texte(taille_case*largeur_plateau/2, taille_case*hauteur_plateau/8, "Normale", taille=50, ancrage = "center",couleur="white")
            texte(taille_case*largeur_plateau/2, 3*taille_case*hauteur_plateau/8, "Terrin torique", taille=50, ancrage = "center")
            texte(taille_case*largeur_plateau/2, 5*taille_case*hauteur_plateau/8, "Obstacle", taille=50, ancrage = "center",couleur="white")
            texte(taille_case*largeur_plateau/2, 7*taille_case*hauteur_plateau/8, "2 joueur", taille=50, ancrage = "center")
            xmode, ymode = attend_clic_gauche()
            if ymode < taille_case*hauteur_plateau/4:
                mode_jeu = 1
            elif ymode < 2*taille_case*hauteur_plateau/4:
                mode_jeu = 2
            elif ymode < 3*taille_case*hauteur_plateau/4:
                mode_jeu = 3
            else:
                mode_jeu = 4
            efface_tout()
        #L'ecran a été divisé en quatre pour une plus grande visibilité pour les joueurs


        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            print(touche(ev))
            direction1 = change_direction1(direction1, touche(ev))
            direction2 = change_direction2(direction2,touche(ev))


        efface_tout()


        #mode de jeu normale: pomme ne disparait pas mais elle vient se rajouter à la tête du serpent pour le faire augmenter de taille
        if mode_jeu==1 or mode_jeu == 2 or mode_jeu == 3:
            # affichage des objets
            affiche_pommes(pommes)


            texte(largeur_plateau*taille_case-150,10,"Score: "+str(score),couleur="black")
            # deplacement du serpent
            x1, y1 = serpent1[0]
            xdir1, ydir1 = direction1
            if (x1+xdir1, y1+ydir1) in pommes:
                pommes.remove((x1+xdir1, y1+ydir1))
                serpent1.insert(0,(x1+xdir1, y1+ydir1))
                score += 1
            elif serpent1.count(serpent1[0]) != 1 or ((x1 < 0 or x1 >= largeur_plateau or y1 < 0 or y1 >= hauteur_plateau) and mode_jeu == 1):
                jouer = False
                affiche_score(score)
            elif mode_jeu == 1:
                serpent1.pop(len(serpent1)-1)
                serpent1.insert(0,(x1+xdir1,y1+ydir1))
        #mode avec terrin torride
            else:
                serpent1.pop(len(serpent1)-1)
                dps_serpent(serpent1, x1, y1, xdir1, ydir1)
            affiche_serpent(serpent1,"green")


        #mode de jeu avec obstacles
        if mode_jeu == 3:
            affiche_obstacle(obstacle,framerate)
            mise_a_jour()
            if (x1, y1) in obstacle:
                jouer = False
                affiche_score(score)

        #Mode de jeu à deux joueurs: les serpents ont une taille initiale et la partie se termine lorque l'un des serpents touche l'autre serpent
        if mode_jeu == 4:
        # affichache des objets
            affiche_serpent(serpent1,"blue")
            affiche_serpent(serpent2,"red")
        # deplacement des serpents
            x1, y1 = serpent1[0]
            x2, y2 = serpent2[0]
            xdir1, ydir1 = direction1
            xdir2, ydir2 = direction2
            if serpent1.count(serpent1[0]) != 1 or serpent1[0] in serpent2:
                jouer = False
                efface_tout()
                texte(taille_case*largeur_plateau/2, taille_case*hauteur_plateau/2, "J2 GAGNE", taille = 70, couleur = "red", ancrage = "center")
                attend_clic_gauche()
            elif serpent2.count(serpent2[0]) != 1 or serpent2[0] in serpent1:
                efface_tout()
                texte(taille_case*largeur_plateau/2, taille_case*hauteur_plateau/2, "J1 GAGNE", taille = 70, couleur = "blue", ancrage = "center")
                jouer = False
                attend_clic_gauche()
            else:
                if direction1 != (0,0) and direction2 != (0,0):
                    dps_serpent(serpent1,x1,y1,xdir1,ydir1)
                    dps_serpent(serpent2,x2,y2,xdir2,ydir2)


        mise_a_jour()


        #Menu de fin
        if jouer == False:
            rectangle(0,0,taille_case*largeur_plateau, taille_case*hauteur_plateau/2, remplissage="black", epaisseur=0)
            rectangle(0, taille_case*hauteur_plateau/2, taille_case*largeur_plateau, taille_case*hauteur_plateau, remplissage="white", epaisseur=0)
            texte(taille_case*largeur_plateau/2, taille_case*hauteur_plateau/4, "Recommencer", taille=50, ancrage = "center",couleur="white")
            texte(taille_case*largeur_plateau/2, 3*taille_case*hauteur_plateau/4, "Quitter", taille=50, ancrage = "center")
            xfin, yfin = attend_clic_gauche()
            compte_fin = 0
            if  yfin < taille_case*hauteur_plateau/2:
                jouer = True
                #Reinitialisation des donnees
                compte_fin = 1
                direction1 = (0, 0)
                direction2 = (0, 0)
                pommes = []
                serpent1 = [(0, 0)]
                serpent2 = [(largeur_plateau-1,hauteur_plateau-1)]
                obstacle = []
                score = 0
                mode_jeu = 0
                efface_tout()
            else:
                compte_fin = 1


        #acceleration
        framerate = 10 + score//2


        # attente avant rafraîchissement
        sleep(1/framerate)

    # fermeture et sortie
    ferme_fenetre()
