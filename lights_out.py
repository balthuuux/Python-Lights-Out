########## Modules ##########
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,RadioButtons
from matplotlib.backend_bases import MouseButton
#############################




########## Fonction de copie de matrice ##########
def copie_matrice(matrice):   # On crée la fonction servant à copier une grille entrée
    '''Fonction qui prend en argument une matrice et la copie dans une autre.'''
    n = len(matrice)
    copie = list()
    for lignes in range(n):
        copie.append(matrice[lignes][:])    
    return copie
##################################################



########## Produit scalaire vecteurs noyau ##########
vecteurs_noyaux = \
    	[[0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0], \
         [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0], \
         [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0], \
         [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1]]

def produit_scalaire(vecteurs_noyaux, matrice):
    '''Fonction qui prend en entrée une grille de départ , mise sous forme de
       vecteur, et les 4 vecteurs du noyau de la matrice résolution 4 * 4 et qui
       effectue le produit scalaire de chaque vecteurs avec la grille de départ.'''
    A = list ()
    for i in range (4):
        A += matrice[i]
    s = 0
    validite = True
    for vecteurs in vecteurs_noyaux :
        for lignes in range (16):
            s += ( vecteurs[lignes] * A[lignes])
        if s%2 != 0:
            validite = False
    return validite
#####################################################
    

    
########## Matrice résolution ##########
def création_matrice(n):
    '''Fonction qui prend en argument une taille et qui crée une matrice nulle de cette taille.'''
    matrice_reso = [[0 for k in range(n)] for k in range(n)]
    return matrice_reso

def reso(matrice_reso, i, j):
    '''Fonction qui prend en argument une matrice de taille n, une ligne et un colonne et qui simule un appuie sur la case_i,j.'''
    n=len(matrice_reso)
    matrice2 = [[0 for k in range(n)] for k in range(n)]
    max = n
    matrice2[i][j] = 1
    if i+1 < max: 
        matrice2[i+1][j] = 1  
    if i-1 >= 0:
        matrice2[i-1][j] = 1
    if j+1 < max:
        matrice2[i][j+1] = 1
    if j-1 >= 0:
        matrice2[i][j-1] = 1
    return matrice2

def compil(matrice_reso):
    '''Fonction qui prend en agument une matrice nulle de taille n et qui 
       compile les fonctions "création_matrice" et "reso" pour créer la matrice
       résolution.'''
    n = len(matrice_reso)
    matrice3 = list()
    for i in range(n):
        for j in range(n):
            liste_tempo = list()
            matrice2 = reso(matrice_reso, i, j)
            
            for k in range(n):
                liste_tempo += matrice2[k]
            matrice3.append(liste_tempo)  
    return matrice3

########## Génération ##########

def generation(taille):   # On génère un grille de taille 3 ou 4
    global vecteurs_noyaux
    '''Fonction qui prend en argument une taille et qui retourne une grille de 
       jeu aléatoire de la taille souhaitée sous forme de matrice.'''
    if taille == 3:   
        grille = [[0 for _ in range(3)] for _ in range(3)]
        for lignes in range(3):
            for colonnes in range(3):
                case = random.randint(0, 1)
                grille[lignes][colonnes] = case
        if grille == [[0 for _ in range(3)] for _ in range(3)]: 
            return generation(taille)
        
    elif taille == 4:
        grille = [[0 for _ in range(4)] for _ in range(4)]
        for lignes in range(4):
            for colonnes in range(4):
                case = random.randint(0, 1)
                grille[lignes][colonnes] = case
        if grille == [[0 for _ in range(4)] for _ in range(4)] or produit_scalaire(vecteurs_noyaux, grille) is False: 
            return generation(taille)
    return grille
########################################



########## Grille 3x3 : pivot de Gauss ##########
def echange_ligne(A, i, j):
    '''Fonction qui prend en argument une matrice, une ligne et une colonne et 
       qui échange la case_i,j et la case_j,i.'''
    A[i], A[j] = A[j], A[i]
    return A

def substitutions_lignes(A, i, j, mu):
    '''Fonction qui prend en argument une matrice, une ligne, une colonne et 
       une constante et qui effectue les substitutions.'''
    for z in range (len(A[i])):
        A[i][z] = round(A[i][z] + mu*A[j][z])%2
    return A

def recherche_pivot(A, i):
    '''Fonction qui prend en argument une matrice, une ligne et qui cherche le 
    coefficient avec la valeur absolue la plus grande.'''
    liste = list()
    for z in range(i, len(A)):
        liste.append([abs(A[z][i]), z])
    liste = max(liste)
    j = liste[1]
    return j

def resolution(Y0, A0):   # Mise sous forme de matrice colonne
    '''Fonction qui prend en argument deux matrice, inverse la seconde puis les 
       multiplie. On utilise pour ça le pivot de Gauss (même si nous somme dans
       le corps de Galois GF(2).'''
    if len(Y0) > 1:   # Permet de passer d'une liste de listes à une liste
        y0 = list()
        for i in Y0:
            y0 += i
        Y0 = y0 
         
    I = [[0 for k in range(len(A0))] for k in range(len(A0))]   # Matrice unité
    for i in range(len(I)):
        I[i][i] = 1
    indexe, p = list(), list()
    
    for i in range(len(A0)):   # Échange des lignes
        P = recherche_pivot(A0, i)
        A0 = echange_ligne(A0, i, P)
        I = echange_ligne(I, i, P)
        
        
    for i in range(len(A0)):   # Indexe des substitutions à effectuer
        for j in range(len(A0)-1):
            v=[k for k in range(len(A0))]
            del v[i]
            l = [v[j], i]
            indexe.append(l)
    
    for i in indexe:   # Substitutions
        p = A0[i[1]][i[1]]
        mu = -((A0[i[0]][i[1]])/p)
        A0 = substitutions_lignes(A0, i[0], i[1], mu)
        I = substitutions_lignes(I, i[0], i[1], mu)
    for i in range(len(A0)):
        mu = (1/A0[i][i])
        for j in range(len(A0)):
            A0[i][j] = round(A0[i][j]*mu)
            I[i][j] = round(I[i][j]*mu)

    m = len(I)   # Produit A**(-1) x B :
    n2 = len(I)
    p = 1
    X = list()           
    for i in range(m):
        for j in range(p):
            S = 0
            for k in range(n2):
                S += (I[i][k] * Y0[k])
            X.append(round(S)%2)
    liste_cases = list()
    x1 = X[:3]
    x2 = X[3:6]
    x3 = X[6:9]
    for i in range(3):
        if x1[i] == 1:
            liste_cases.append([0, i])
        if x2[i] == 1:
            liste_cases.append([1, i])
        if x3[i] == 1:
            liste_cases.append([2, i])
    liste_cases.sort()
    return liste_cases
################################



########## Grille 4x4 : brute-force ##########
def appui(matrice, parcours = [[-1, -1]], iteration = 0):   # Une liste de liste rempli de 1 pour une longueur non-nul lors du "for i in..."
    '''Fonction qui prend en argument une matrice, un historique de parcours et
       une itération et qui simule un appui sur chaque case à l'iteration 
       actuelle.'''
    n = len(matrice)
    longueur = len(parcours)   # Taille du parcours, nombre de cases parcourus
    liste_grille = list()
    
    liste = list()   # On crée la liste servant à enregistrer les toutes premières positions
    if iteration == 0:   # On utilise ce critère pour créer la première liste des positions
        for lignes in range(n):
            for colonnes in range(n):
                liste.append([lignes, colonnes])            
    
    i = 0            
    
    for lignes in range(n):
        for colonnes in range(n):
            
                                  
            copie = copie_matrice(matrice)   # On copie la grille pour ne pas appuyer sur toute les case de la même grille
            copie_parcours = copie_matrice(parcours)   # On copie le parcours pour ne pas y entrer toutes les positions mais bien celle prise
            copie_parcours = copie_parcours + [[]]   # On concatène une liste vide pour pouvoir ajouter la case touchée, et ceci à chaque iteration
            
            valeur = True   # On met valeur à False par defaut
            for case in range(longueur):   
#                if parcours[case][0] == lignes and parcours[case][1] == colonnes :   # On vérifi si les cases n'ont pas déjà été appuyées                    
                if lignes < parcours[case][0] or lignes <= parcours[case][0] and colonnes <= parcours[case][1] : 
                    valeur = False
                
                
            if valeur is True:
                
                copie[lignes][colonnes] = (copie[lignes][colonnes]+1)%2
                if lignes+1 < n: 
                    copie[lignes+1][colonnes] = (copie[lignes+1][colonnes]+1)%2
                if lignes-1 >= 0:
                    copie[lignes-1][colonnes] = (copie[lignes-1][colonnes]+1)%2
                if colonnes+1 < n:
                    copie[lignes][colonnes+1] = (copie[lignes][colonnes+1]+1)%2
                if colonnes-1 >= 0:
                    copie[lignes][colonnes-1] = (copie[lignes][colonnes-1]+1)%2 
                    
                copie_parcours[longueur] = [lignes, colonnes]   # On ajoute la case touchée au parcours
                    
                if iteration == 0:   
                    copie_parcours[0] = liste[i]   # On rentre les premières cases appuyées dans le parcours                    
                    del copie_parcours[1]   # On supprime donc les -1...
                i+=1
                    
                liste_grille.append([copie, copie_parcours, iteration])   # On incrémentera "iteration" de 1 (elle ne dépassera donc pas n²)    
                    
                    
    return liste_grille


# On crée deux fonctions (dont une récursive) qui relancent le programme jusqu'à ce que la solution soit trouvée (ou non !)

def compilation(liste_de_grille):
    '''Fonction qui prend en argument une liste de grille et qui relance la 
       fonction "appui" pour chacune des grilles.'''
    liste = list()
    for listes in liste_de_grille :   # On trie toute les variables
        grille = listes[0]
        parcours = listes[1]    
        iteration = listes[2] + 1
        n = len(grille)
        
        if grille == [[0 for _ in range(n)] for _ in range(n)]:
            return [True, parcours]
        elif iteration >= 16:
            return [False, parcours]
        
        nouvelle_grille = appui(grille, parcours, iteration)
        liste += brute_force(nouvelle_grille)   # On ajoute en bout de liste car on ne veut pas segmenter par cases
    
    return compilation(liste)
        
        
def brute_force(liste_de_grille):
    '''Fonction qui prend en argument une liste de grille et qui relance la 
       fonction "appui" pour chaqu'une des grilles
       (fonction complémentaire de "compilation").'''
    nouvelle_grille = list()   # On ajoute dans cette liste les grilles crées  
    for listes in liste_de_grille : 
        grille = listes[0]
        parcours = listes[1]    
        iteration = listes[2] 
        
        nouvelle_grille.append([grille, parcours, iteration])
    
    return nouvelle_grille
##############################################



########## Interface Graphique ##########
def affichage(grille):
    '''Fonction qui prend en argument une grille et qui affiche la grille de 
    jeu, les cases, les étoiles et les boutons. C'est l'interface graphique 
    du jeu.'''
    
    fig.clf()
    
    global grille_g, cases_victoire_g   # Boutons / Grille / fig
    aide_axe = plt.axes([0.4, 0.07, 0.2, 0.08])
    bouton_aide = Button(aide_axe, 'Solve', color="aliceblue", hovercolor="cornflowerblue")
    bouton_aide.on_clicked(aide)
    
    main_axe = plt.axes([0.1, 0.2, 0.8, 0.68])   # axe du plot (jeu)
    main_axe.axis("off")
    main_axe.axis("equal")
    
    n = len(grille)   # Tracé de la grille 
    for i in range(n+1):
        x,y = [],[]
        X,Y = [],[]
        for j in range(n+1):
            x.append(i)
            y.append(j)
            X.append(j)
            Y.append(i)
        main_axe.plot(x,y,color = "cornflowerblue",lw = 3)
        main_axe.plot(X,Y,color = "cornflowerblue",lw = 3)
    main_axe.axis("off")
    main_axe.axis("equal")
    plt.draw()
    
    if grille == [[0 for _ in range(n)] for _ in range(n)]:   # Affichage des cases
        plt.title("Gagné !!!", fontsize=15, color = 'royalblue')
        plt.title("Ne quittez pas maintenant", loc='right', color='red', fontsize=12, y=-0.05)
        
        Yposition = int(n) + 0.5
        for l in range(n):
            Xposition = 0.5
            Yposition = Yposition -1
            for k in range(n):
                if n == 3:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'grey',markersize =61.1)
                elif n ==4:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'grey',markersize =45.1)
                Xposition += 1  
                
        plt.pause(1.5)
        fig.clf() 
         
        radio_axe2 = plt.axes([0.05, 0.44 , 0.15, 0.2])   # axes des boutons
        play_axe2 = plt.axes([0.4, 0.07, 0.2, 0.08])
        
        radio_button2 = RadioButtons(radio_axe2, ("3x3","4x4"))   # boutons 
        bouton_play2 = Button(play_axe2, 'PLAY !', color="aliceblue", hovercolor="cornflowerblue")
        
        def start2(val):
            '''Fonction qui lance la fonction "jouer" avec la taille du radio 
               bouton.'''
            return jouer(radio_button2.value_selected)
        
        main_axe = plt.axes([0.1, 0.2, 0.8, 0.68]) 
        main_axe.axis("off")
        main_axe.axis("equal")
        main_axe.set_title("Nouvelle partie", color='royalblue', fontsize=18)
        
        bouton_play2.on_clicked(start2)
        plt.draw()
        
    elif n==3:
        plt.title("Lights Out 3x3", fontsize=15, color = 'royalblue')
        plt.title("Clic droit pour les cases", loc='right', color='green', fontsize=12, y=-0.05)
        Yposition = 3.5        
        for l in range(n):
            Xposition = 0.5
            Yposition = Yposition -1
            for k in range(n):
                if grille[l][k]%2 == 1:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'yellow', markersize =61.1)   
                else:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'grey', markersize =61.1) 
                if grille[l][k] != 0 and grille[l][k] != 1:
                    plt.plot(Xposition,Yposition,marker = '*',color = 'red', markersize =20)
                Xposition += 1   
                
    elif n==4:
        plt.title("Lights Out 4x4", fontsize=15, color = 'royalblue')
        plt.title("Clic droit pour les cases", loc='right', color='green', fontsize=12, y=-0.05)
        Yposition = 4.5
        for l in range(n):
            Xposition = 0.5
            Yposition = Yposition -1
            for k in range(n):
                if grille[l][k]%2 == 1:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'yellow',markersize = 45.1)
                else:
                    plt.plot(Xposition,Yposition,marker = 'o',color = 'grey',markersize = 45.1)
                if grille[l][k] != 0 and grille[l][k] != 1:
                    plt.plot(Xposition,Yposition,marker = '*',color = 'red',markersize =15)
                Xposition += 1  
                     
        
    return clicks()


def clicks():   # Detecte les cases afféctées par le touché
    '''Fonction qui simule les clics de la grille de l'interface graphique.'''
    global grille_g
    mouse_click = [plt.ginput(n=1, timeout=0, show_clicks=True, mouse_add=MouseButton.RIGHT, mouse_pop=MouseButton.LEFT)[0]]
    grille = grille_g
    n = len(grille)
    for click in mouse_click:
        cases = []
        
        if (click[0]>0 and click[0]<n) and (click[1]>0 and click[1]<n):
            if (click[0] >= 0 and click[0] <= n) and (click[1] >= 0 and click[1] <= n):   # Case touchée
                cases.append([int((n-1)-(click[1]//1)), int(click[0]//1)])
            if (click[0]+1 >= 0 and click[0]+1 <= n) and (click[1] >= 0 and click[1] <= n):   # Case droite
                cases.append([int((n-1)-((click[1]//1))), int((click[0]+1)//1)])
            if (click[0]-1 >= 0 and click[0]-1 <= n) and (click[1] >= 0 and click[1] <= n):   # Case gauche
                cases.append([int((n-1)-((click[1]//1))), int((click[0]-1)//1)])
            if (click[0] >= 0 and click[0] <= n) and (click[1]+1 >= 0 and click[1]+1 <= n):   # Case haut
                cases.append([int((n-2)-((click[1]//1))), int(click[0]//1)])
            if (click[0] >= 0 and click[0] <= n) and (click[1]-1 >= 0 and click[1]-1 <= n):   # Case bas
                cases.append([int((n)-((click[1]//1))), int(click[0]//1)])
        
        
        val = False   # On verifi si la case touchée a une étoile (si le jeu est en mode "aide")
        sol = False
        if cases != []:
            for lignes in range(n):   # On change les valeurs des cases afféctées
                for colonnes in range(n):
                    if 2 in grille[lignes] or 3 in grille[lignes]:
                        sol = True
        for lignes in range(n):   # On change les valeurs des cases afféctées
            for colonnes in range(n):
                if sol is True:
                    if [lignes, colonnes] == cases[0]:
                        val = True
                        val_case = grille[lignes][colonnes]
                        pos = [lignes, colonnes]
        
        if cases != []:   # On modifi la valeur de la case touché si elle à une étoile pour l'éteindre
            if grille[cases[0][0]][cases[0][1]] == 3:
                grille[cases[0][0]][cases[0][1]] = 1
            elif grille[cases[0][0]][cases[0][1]] == 2:
                grille[cases[0][0]][cases[0][1]] = 0
                
        for lignes in range(n):   # On change les valeurs des autres cases afféctées
            for colonnes in range(n):
                if [lignes, colonnes] in cases:
                    if grille[lignes][colonnes] == 3:
                        grille[lignes][colonnes] = 2
                    elif grille[lignes][colonnes] == 2:
                        grille[lignes][colonnes] = 3
                    else:
                        grille[lignes][colonnes] = (grille[lignes][colonnes]+1)%2 
                        
        if val is True:   # On ajoute une étoile à la case touché si elle n'en avais pas (fausse manipulation)
            if val_case == 0:
                grille[pos[0]][pos[1]] = 3
            elif val_case == 1:
                grille[pos[0]][pos[1]] = 2               
    grille_g = grille
    return affichage(grille)
    
def jouer(taille):   # selectionne la grille à jouer / lance affichage
    '''Fonction qui prend en argument une taille et qui sélectionne la grille 
       de la taille souhaité à jouer puis qui lance l'affichage.'''
    global grille_g, grille_depart_g, taille_g
    taille_g = taille
   
    if taille == "3x3":
        grille = generation(3)
    elif taille == "4x4":
        grille = generation(4)
    grille_g = grille
    grille_depart_g = copie_matrice(grille)
    return affichage(grille)
#########################################
        
    

############ GLOBAL ############
grille_g = list()
grille_depart_g = list()
taille_g = str()
cases_victoire_g = list()
################################



############ BASE DU JEU ############
fig = plt.figure()   # Fig de départ

def aide(val):   # Affichage de la solution
    '''Fonction qui lance la fonction "aider" au clic du wiget SOLVE.'''
    global grille_g, taille_g
    return aider(grille_g, taille_g)

def aider(grille, taille):   # affiche les étoiles
    '''Fonction qui prend en argument une grille et une taille et qui va 
       calculer ses solutions.'''
    global cases_victoire_g, grille_g
    n = len(grille)
    chgmt = False
    for lignes in grille:
        if 2 in lignes or 3 in lignes:
            chgmt = True
    cases_a_toucher = False
    if chgmt is True:
        for lignes in range(n):
            for colonnes in range(n):
                grille[lignes][colonnes] %= 2
                cases_a_toucher = list()
    elif taille == "3x3":
        matrice_reso = compil(création_matrice(3))   # création de la matrice résolution
        cases_a_toucher = resolution(grille, matrice_reso)
    elif taille == "4x4":
        if grille != [[0 for _ in range(4)] for _ in range(4)]:
            cases_a_toucher = compilation(appui(grille))[1]
        else: 
            cases_a_toucher = False
    for i in cases_a_toucher:
            if grille[i[0]][i[1]] == 0:
                grille[i[0]][i[1]] = 2
            else:
                grille[i[0]][i[1]] = 3
    cases_victoire_g = cases_a_toucher   # On rafraichit le global
    grille_g = grille
    return affichage(grille)

def start(val):   # Lancer le jeu
    '''Fonction qui lance la fonction "jouer" au clic du wiget PLAY !.'''
    return jouer(radio_button.value_selected)
  

radio_axe = plt.axes([0.05, 0.44 , 0.15, 0.2])   # axes des boutons 
play_axe = plt.axes([0.4, 0.07, 0.2, 0.08])

radio_button = RadioButtons(radio_axe, ("3x3","4x4"))   # boutons 
bouton_play = Button(play_axe, 'PLAY !', color="aliceblue", hovercolor="cornflowerblue")

main_axe = plt.axes([0.1, 0.2, 0.8, 0.68])   # axes pour tracer la grille
main_axe.axis("off")
main_axe.axis("equal")
main_axe.set_title("'Tricher au jeu sans gagner est d'un sot.'", color='royalblue', fontsize=18)

bouton_play.on_clicked(start)
plt.show()
#####################################
