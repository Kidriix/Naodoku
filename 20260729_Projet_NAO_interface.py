import pandas as pd
import altair as alt
import streamlit as st
import os
import numpy as np
from datetime import datetime


st.cache_data.clear()
submitted = False

st.set_page_config(page_title="DEMO", layout="centered")
st.markdown("""
<style>
/* Force les variables de thème clair, peu importe data-theme */
:root, .stApp, [data-theme="dark"] {
    --background-color: #FFFFFF !important;
    --secondary-background-color: #F0F2F6 !important;
    --text-color: #31333F !important;
    --primary-color: #228B22 !important;
}

.stApp {
    background-color: #FFFFFF !important;
    color: #31333F !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F0F2F6 !important;
}
section[data-testid="stSidebar"] * {
    color: #31333F !important;
}

/* Inputs, selects, textareas */
input, textarea, select {
    background-color: #FFFFFF !important;
    color: #31333F !important;
}

/* Header en haut */
header[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
}
.stApp {
    background-color: #FFFFFF;
    color: #31333F;
}

/* Boutons */
.stButton > button:hover {
    background-color: #FFFFFF;
    color: #228B22;
    border: 1px solid #228B22;
}

/* Liens */
a {
    color: #228B22 !important;
}

/* Sliders */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #228B22;
}
div[data-baseweb="slider"] div[style*="background"] {
    background-color: #228B22;
}

/* Checkbox et radio (coché) */
input[type="checkbox"]:checked,
input[type="radio"]:checked {
    accent-color: #228B22;
}

/* Barre de progression */
div[data-testid="stProgress"] > div > div {
    background-color: #228B22;
}

/* Spinner de chargement */
div[data-testid="stSpinner"] > div {
    border-top-color: #228B22 !important;
}

/* Puces de liste à cocher / selectbox sélectionné */
div[data-baseweb="select"] [aria-selected="true"] {
    background-color: #228B22 !important;
    color: #FFFFFF !important;
}

/* Onglets actifs (tabs) */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #228B22 !important;
    border-bottom-color: #228B22 !important;
}
div[data-testid="stAlert"] {
    background-color: #E6F4EA !important;
    border-left: 5px solid #34A853;
}
div[data-testid="stAlert"] p {
    color: #1E4620 !important;
}
li::marker {
    color: #34A853 !important;
}
li {
    color: #31333F !important;
}
</style>
""", unsafe_allow_html=True)

refresh = False
grids = pd.read_csv("20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv("20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv("20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')

stations_names = [" "] + sorted(truth_table["Nom arret"].tolist())
st.session_state.stations_names = stations_names
row_letters = ["D", "E", "F"]
col_letters = ["A", "B", "C"]

def pick_random_grid():
    a = np.random.randint(len(grids))
    selected_grid = grids.iloc[int(a)]

    return selected_grid

def get_possible_stations(crit1, crit2):
  possible_list = sorted(truth_table[(truth_table[crit1] == "VRAI") & (truth_table[crit2] == "VRAI")]["Nom arret"].tolist())
  return possible_list

def get_grid_possibilities(given_grid):
  all_possibilities = {}
  for col in col_letters:
    col_name = given_grid[f"Criteria {col}"]
    for row in row_letters:
      row_name = given_grid[f"Criteria {row}"]
      poss_list =  get_possible_stations(col_name, row_name)
      all_possibilities[col+row]=poss_list
  return all_possibilities

if "grid" not in st.session_state:
    st.session_state.grid = pick_random_grid()

if "grid_answers" not in st.session_state:
    st.session_state.grid_answers = get_grid_possibilities(st.session_state.grid)

if "stations_options" not in st.session_state:
    st.session_state.stations_options = st.session_state.stations_names

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "errors" not in st.session_state:
    st.session_state.errors = 0

if "end_game" not in st.session_state:
    st.session_state.end_game = False

def is_cell_okay(crit_col, crit_row, cell):
  crit_col_status = truth_table[truth_table["Nom arret"] == cell][crit_col].tolist()[0]
  crit_row_status = truth_table[truth_table["Nom arret"] == cell][crit_row].tolist()[0]
  if (crit_col_status == "VRAI") & (crit_row_status == "VRAI"):
     return True
  else : 
     return False

def launch_new_game():
  st.session_state.grid = pick_random_grid()
  st.session_state.end_game = False
  st.session_state.user_answers = {}
  st.session_state.grid_answers = get_grid_possibilities(st.session_state.grid)
  st.session_state.errors = 0
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

def reload_same_game():
  st.session_state.user_answers = {}
  st.session_state.errors = 0
  st.session_state.end_game = False
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

def give_up():
  st.session_state.end_game = True
  st.rerun()

@st.dialog("Choisir un arrêt")
def select_station(col, row):
    crit_col = st.session_state.grid[f"Criteria {col}"]
    crit_row = st.session_state.grid[f"Criteria {row}"]
    st.markdown(f"Sélectionner un arrêt vérifiant **{crit_col}** et **{crit_row}**")
    station = st.selectbox(label=f"{len(st.session_state.grid_answers[col+row])} arrêts possibles", options=st.session_state.stations_options, key=col+row)
    stop_cols = st.columns(2)
    if stop_cols[0].button("Valider", type="primary", key=f"valider_{col+row}"):
      if station == " ":
        st.warning("Aucun arrêt sélectionné")
      else:
        if is_cell_okay(crit_col, crit_row, station):
            st.session_state.user_answers[col+row] = station
            st.session_state.stations_options.remove(station)
        else :
            st.session_state.errors += 1
        st.rerun()
    if stop_cols[1].button("Annuler", key=f"annuler_{col+row}"):
      st.session_state.__delattr__(col+row)
      st.rerun()

@st.dialog("Voir les solutions")
def check_answers(col, row):
  crit_col = st.session_state.grid[f"Criteria {col}"]
  crit_row = st.session_state.grid[f"Criteria {row}"]
  st.markdown(f"Liste des arrêts vérifiant **{crit_col}** et **{crit_row}**")
  cell_answers = st.session_state.grid_answers[col+row]
  for station in cell_answers:
    st.markdown(station)
  if st.button("Fermer", key=f"close_answers_{col+row}"):
    st.rerun()

@st.dialog("Bravo !")
def bravo():
  st.balloons()
  st.markdown('''
  Grille complète, bravo !
  ''')
  win_cols = st.columns(4)
  if win_cols[0].button("Nouvelle grille", key="new_grid_replay_win", type="primary"):
    launch_new_game()
  if win_cols[1].button("Rejouer la grille", key="same_grid_replay_win"):
    reload_same_game()
  if win_cols[2].button("Voir les solutions", key="check_answers_win"):
    st.rerun()
  if win_cols[3].button("Ballons :)", key="balloons_win"):
    st.balloons()

@st.dialog("Dommage...")
def you_lose():
  st.markdown('''
  Dommage : 3 erreurs, c'est perdu
  ''')
  lose_cols = st.columns(3)
  if lose_cols[0].button("Nouvelle grille", key="new_grid_replay_lose"):
    launch_new_game()
  if lose_cols[1].button("Rejouer la grille", key="same_grid_replay_lose"):
    reload_same_game()
  if lose_cols[2].button("Voir les solutions", key="check_answers_lose"):
    st.rerun()

@st.dialog("Confirmation")
def are_you_sure(action, action_func):
  st.markdown(f'''
  Êtes-vous sûr.e de vouloir **{action}** ?
  
  Cela mettra fin à la partie en cours.
  ''')
  confirm_cols = st.columns(2)
  if confirm_cols[0].button("Confirmer", key=f"confirm", type="primary"):
    action_func()
  if confirm_cols[1].button("Annuler", key=f"cancel"):
    st.rerun()

st.header('''
:green[**NAODOKU**]
''')
st.info('''
Bienvenue sur Naodoku, le "sudoku" Naolib !

Comment ça marche ?
- Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway et/ou Busway du réseau Naolib tout en respectant les critères de la ligne et de la colonne.
- Une fois entré, un arrêt ne peut plus être ni modifié, réutilisé ailleurs dans la grille.
- La partie se termine une fois les 9 cases complétées ou après 3 erreurs.
- Si une catégorie n'est pas claire, une petite bulle d'aide permet d'afficher une explication.
- A la fin de la partie, les solutions seront consultables par case.

Concept calqué sur [**métrodoku**](https://www.metrodoku.fr) en version Nantaise.

Bon jeu !

PS : Le projet est encore *relativement* bancal et le dev du jeu n'étant pas dev de métier merci d'être indulgent :) 
''')
st.link_button(label="Lien Métrodoku", url="https://www.metrodoku.fr")

with st.container(border = True):
  st.markdown("C'est le menu")
  bottom_cols = st.columns(3)
  if bottom_cols[0].button(":heavy_plus_sign: Générer une nouvelle grille", key="new_grid_reset"):
    are_you_sure("Générer une nouvelle grille", launch_new_game)
  if bottom_cols[1].button(":repeat: Réinitialiser la grille", key="same_grid_reset"):
    are_you_sure("Réinitialiser la grille", reload_same_game)
  if not st.session_state.end_game :
    if bottom_cols[2].button(":x: Abandonner et voir les résultats", key="give_up"):
      are_you_sure("Abandonner et voir les résultats", give_up)

st.markdown("Nombre d'erreurs (max 3): ")
err_cols = st.columns(3, gap="small", border= False)
err_col_ception = err_cols[0].columns(3, gap="small", border= True)
for i in range(st.session_state.errors):
  err_col_ception[i].markdown(":x:")

for row in range(4):
  grid_cols = st.columns(4, border = True)
  if row == 0:
    for (i, let_col) in enumerate(col_letters):
      with grid_cols[i + 1].container(border= True):
        st.markdown(f"**{st.session_state.grid[f"Criteria {let_col}"]}**", help=legend[legend["Nom critere"]==st.session_state.grid[f"Criteria {let_col}"]]["Description"].tolist()[0])
  else: 
    row_let = row_letters[row-1]
    with grid_cols[0].container(border= True):
        st.markdown(f"**{st.session_state.grid[f"Criteria {row_let}"]}**", help=legend[legend["Nom critere"]==st.session_state.grid[f"Criteria {row_let}"]]["Description"].tolist()[0])
    for (i, col_let) in enumerate(col_letters):
      cell_id = col_let + row_let
      if not st.session_state.end_game:
        if cell_id not in st.session_state.user_answers:
          button = grid_cols[i + 1].button(label=f"{len(st.session_state.grid_answers[cell_id])} arrêts possibles", key=cell_id+"_answer_button", on_click=select_station, kwargs={"col": col_let, "row": row_let})
        else : 
          grid_cols[i + 1].markdown(st.session_state.user_answers[cell_id])
      else :
        button = grid_cols[i + 1].button(label=f"Voir les {len(st.session_state.grid_answers[cell_id])} solutions", key=cell_id+"_endgame_button", on_click=check_answers, kwargs={"col": col_let, "row": row_let})

if (len(st.session_state.user_answers) == 9) & (not st.session_state.end_game):
  st.session_state.end_game = True
  bravo()

if (st.session_state.errors == 3) & (not st.session_state.end_game):
  st.session_state.end_game = True
  you_lose()
