difficulty_explanation = '''
**Méthode d'estimation de la difficulté d'une grille**

Chaque case de la grille comporte un nombre de réponses possibles. 
En fonction de ce nombre, on associe un score de difficulté à la case selon le barème suivant :
- 1 à 5 réponses possibles : 5 points
- 6 à 10 réponses possibles : 4 points
- 11 à 15 réponses possibles : 3 points
- 16 à 20 réponses possibles : 2 points
- 21 ou plus réponses possibles : 1 point

La somme des scores des 9 cases donne une note sur 45, ramenée en note sur 5 puis arrondie au 0.5 le plus proche.

**Limites** : 
La méthode ne prend pas en compte le contenu des critères des cases, qui jouent un rôle dans la difficulté réelle.
'''

you_lose_text = '''
  Dommage : 3 erreurs, c'est perdu
  '''

intro_text_1 = '''
    Bienvenue sur Naodoku, le "sudoku" Naolib !

    Comment ça marche ?
    - Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway (Lignes 1, 2 et 3) et/ou Busway (Lignes 4 et 5) du réseau Naolib.
    
    '''

intro_text_2 = '''
    - Un arrêt est valide dans une case si il respecte à la fois les critères de la ligne et de la colonne.
    - Une fois entré, un arrêt ne peut plus être ni modifié, réutilisé ailleurs dans la grille.
    - La partie se termine une fois les 9 cases complétées ou après 3 erreurs.
    - Si une catégorie n'est pas claire, cliquer sur la catégorie permet d'afficher une explication.
    - A la fin de la partie, les solutions seront consultables par case.

    Concept calqué sur [**métrodoku**](https://www.metrodoku.fr) en version Nantaise.

    Bon jeu !

    PS : Le projet est encore *relativement* bancal et le dev du jeu n'étant pas dev de métier merci d'être indulgent :) 
    '''

intro_hints_text = '''
    Vous disposez de **3 indices** par partie afin de vous aider. 
      - Il existe 3 types d'indices, chacun utilisable une seule fois par partie.
      - Il n'est possible d'utiliser **qu'un seul indice** par case.
'''

hint_1_text = '''
    Pour chacun des arrêts possibles, la première lettre de chaque mot du nom est révélée. 
    Un emplacement vide est indiqué pour chacune des autres lettres, à la manière d'un jeu de Pendu. 
    Les signes de ponctuation éventuels sont conservés.

    *Exemple* :  **Porte de Vertou** devient **P____ d_ V_____** 
'''

hint_2_text = '''
    Pour chacun des arrêts possibles, toutes les lignes qui le desservent sont révélées.

    *Exemple* : **Aimé Delrue** --> **Ligne 2** et **Ligne 3**
'''

hint_3_text = '''
    Une sélection de 4 arrêts est affichée. Parmi eux, seul 1 est valide.
    Les 3 autres propositions ne respectent qu'un seul des 2 critères de la case.

    *Exemple pour une case "Sur la ligne de Tramway 2" et "Sud Loire"* :

    Porte de Vertou (Ligne 4 et **Sud Loire**)
    
    **Pirmil** (**Ligne 2** et **Sud Loire**)
    
    Neustrie (Ligne 3 et **Sud Loire**)
    
    50 otages (**Ligne 2** et Nord Loire)
'''