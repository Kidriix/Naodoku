from constants.ref_files_paths import *

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

you_lose_text_errors = '''
  3 erreurs, c'est perdu :(
  '''

you_lose_text_zero_answer_cell = '''
  C'est perdu :(
  
  Toutes les solutions des cases suivantes ont été épuisées (utilisées ailleurs):
'''

thanks_text = '''
  Merci d'avoir joué !
'''

intro_text_1 = f'''
    Bienvenue sur Naodoku, le "sudoku" Naolib !

    Comment ça marche ?
    - Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway {lines_emojis_list[0]} {lines_emojis_list[1]} {lines_emojis_list[2]} et/ou Busway {lines_emojis_list[3]} {lines_emojis_list[4]} du réseau Naolib.
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
    Vous disposez de **3 indices** par partie afin de vous aider :
      - Les indices sont disponibles pour toute case comportant 5 solutions ou moins.
      - Il existe 3 types d'indices, chacun utilisable une seule fois par partie.
      - Il n'est possible d'utiliser **qu'un seul indice** par case.
'''

hint_1_text = '''
    Pour chacun des arrêts possibles, la première lettre de chaque mot du nom est révélée. 
    Un emplacement vide est indiqué pour chacune des autres lettres, à la manière d'un jeu de Pendu. 
    Les signes de ponctuation éventuels sont conservés.

    *Exemple* :  **Porte de Vertou** devient **P____ d_ V_____** 
'''

hint_2_text = f'''
    Pour chacun des arrêts possibles, toutes les lignes qui le desservent sont révélées.

    *Exemple* : **Aimé Delrue** -> {lines_emojis_list[1]} et {lines_emojis_list[2]}
'''

hint_3_text = f'''
    Une sélection de 4 arrêts est affichée. Parmi eux, seul 1 est valide.
    Les 3 autres propositions ne respectent qu'un seul des 2 critères de la case.

    *Exemple pour une case "Sur la ligne de Tramway {lines_emojis_list[1]}" et "Sud Loire"* :

    Porte de Vertou ({lines_emojis_list[3]} et **Sud Loire**) -> :x:
    
    **Pirmil** ({lines_emojis_list[1]} et **Sud Loire**) -> :white_check_mark: 
    
    Neustrie ({lines_emojis_list[2]} et **Sud Loire**) -> :x:
    
    50 otages ({lines_emojis_list[1]} et Nord Loire) -> :x:
'''
