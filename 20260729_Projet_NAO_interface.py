import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
from datetime import datetime

st.set_page_config(page_title="NAO_DEMO", layout="centered")

grids = pd.read_csv("20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv("20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv("20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')

if "first_opening" not in st.session_state:
    st.session_state.first_opening = True

stations_names = [" "] + sorted(truth_table["Nom arret"].tolist())
st.session_state.stations_names = stations_names
row_letters = ["D", "E", "F"]
col_letters = ["A", "B", "C"]

clickable_ids = {5, 6, 7, 9, 10, 11, 13, 14, 15}  
criteria_ids = {1, 2, 3, 4, 8, 12}
grid_ids_to_letters = {1:"A", 2:"B", 3:"C", 4:"D", 5:"AD", 6:"BD", 7:"CD", 8:"E", 9:"AE", 10:"BE", 11:"CE", 12:"F", 13:"AF", 14:"BF", 15:"CF"}

@st.dialog("Bienvenue")
def welcome():
    st.info('''
        Bienvenue sur Naodoku, le "sudoku" Naolib !

        Comment ça marche ?
        - Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway (Lignes 1, 2, 3) et/ou Busway (Lignes 4 et 5) du réseau Naolib tout en respectant les critères de la ligne et de la colonne.
        - Une fois entré, un arrêt ne peut plus être ni modifié, réutilisé ailleurs dans la grille.
        - La partie se termine une fois les 9 cases complétées ou après 3 erreurs.
        - Si une catégorie n'est pas claire, cliquer sur la catégorie permet d'afficher une explication.
        - A la fin de la partie, les solutions seront consultables par case.

        Concept calqué sur [**métrodoku**](https://www.metrodoku.fr) en version Nantaise.

        Bon jeu !

        PS : Le projet est encore *relativement* bancal et le dev du jeu n'étant pas dev de métier merci d'être indulgent :) 
        ''')
    st.session_state.first_opening = False

@st.dialog("Description")
def describe_criteria(cell_id):
   desc = legend[legend["Nom critere"]==st.session_state.grid[f"Criteria {grid_ids_to_letters[cell_id]}"]]["Description"].tolist()[0]
   st.markdown(desc)

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

if "last_clicked" not in st.session_state:
    st.session_state["last_clicked"] = None

if "clickable_ids" not in st.session_state:
    st.session_state.clickable_ids = clickable_ids

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
  st.session_state.clickable_ids = clickable_ids
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

def reload_same_game():
  st.session_state.user_answers = {}
  st.session_state.errors = 0
  st.session_state.end_game = False
  st.session_state.clickable_ids = clickable_ids
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

def give_up():
  st.session_state.end_game = True
  st.rerun()

@st.dialog("Choisir un arrêt")
def select_station(cell_id):
    col, row = grid_ids_to_letters[cell_id][0], grid_ids_to_letters[cell_id][1]
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
            st.session_state.clickable_ids.remove(cell_id)
        else :
            st.session_state.errors += 1
        st.rerun()
    if stop_cols[1].button("Annuler", key=f"annuler_{col+row}"):
      st.session_state.__delattr__(col+row)
      st.rerun()

@st.dialog("Voir les solutions")
def check_answers(cell_id):
  col, row = grid_ids_to_letters[cell_id][0], grid_ids_to_letters[cell_id][1]
  crit_col = st.session_state.grid[f"Criteria {col}"]
  crit_row = st.session_state.grid[f"Criteria {row}"]
  st.markdown(f"Liste des arrêts vérifiant **{crit_col}** et **{crit_row}**")
  cell_answers = st.session_state.grid_answers[col+row]
  for station in cell_answers:
    with st.container(border=True, key="container_"+station):
        st.markdown(station)

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
    st.session_state.clickable_ids = clickable_ids
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
    st.session_state.clickable_ids = clickable_ids
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


labels = []
for i in range(16):
    if i == 0:
        labels.append("**NAODOKU**")
    elif len(grid_ids_to_letters[i]) == 1:
        labels.append(f"**{st.session_state.grid[f"Criteria {grid_ids_to_letters[i]}"]}**")
    elif grid_ids_to_letters[i] in st.session_state.user_answers :
        labels.append(st.session_state.user_answers[grid_ids_to_letters[i]])
    else : 
        labels.append(f"{len(st.session_state.grid_answers[grid_ids_to_letters[i]])} arrêts possibles")

st.session_state.labels = labels

max_len = max(len(l) for l in st.session_state.labels)
if max_len <= 15:
    uniform_font_size = "clamp(0.6rem, 3vw, 0.95rem)"
elif max_len <= 30:
    uniform_font_size = "clamp(0.5rem, 2.3vw, 0.78rem)"
elif max_len <= 45:
    uniform_font_size = "clamp(0.42rem, 1.9vw, 0.65rem)"
else:
    uniform_font_size = "clamp(0.36rem, 1.6vw, 0.55rem)"


color_naodoku_bg     = "#b9f2c4"  
color_naodoku_text   = "#1a5c2e"
color_criteria      = "#eef0f4"  
color_criteria_text = "#333"
color_criteria_border = "#000000"
color_empty         = "#FFFFFF"  
color_empty_text    = "#000000"
color_empty_border = "#2E7D32"
color_filled        = "#b9f2c4"  
color_filled_text   = "#1a5c2e"
color_filled_border = "#2E7D32"

extra_css = ""
extra_css += f"""
    .st-key-cell_{0} button, .st-key-cell_{0} button:disabled {{
        background-color: {color_naodoku_bg} !important;
        color: {color_naodoku_text} !important;
    }}"""
for i in criteria_ids:
    extra_css += f"""
    .st-key-cell_{i} button, .st-key-cell_{i} button:disabled {{
        background-color: {color_criteria} !important;
        color: {color_criteria_text} !important;
        border: 1px solid {color_criteria_border} !important;
    }}"""

for i in clickable_ids:
    col_row = grid_ids_to_letters[i]
    if col_row in st.session_state.user_answers:
        extra_css += f"""
    .st-key-cell_{i} button, .st-key-cell_{i} button:disabled {{
        background-color: {color_filled} !important;
        color: {color_filled_text} !important;
        border: 1px solid {color_filled_border} !important;
    }}"""
    else:
        extra_css += f"""
    .st-key-cell_{i} button, .st-key-cell_{i} button:disabled {{
        background-color: {color_empty} !important;
        color: {color_empty_text} !important;
        border: 1px solid {color_empty_border} !important;
    }}"""

st.markdown(f"""
<style>
:root {{
    --cell-size: min(20vw, 100px);
}}
[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {{
    max-width: 480px;
    margin: 0 auto;
    flex-wrap: nowrap !important;
    gap: min(2vw, 10px) !important;
}}
[data-testid="stHorizontalBlock"] > [data-testid="column"] {{
    width: 25% !important;
    flex: 1 1 25% !important;
    min-width: 0 !important;
    min-height: 0 !important;
    padding: 0 2px !important;
}}
/* min-height: 0 sur TOUTE la chaîne de conteneurs flex parents/enfants */
div[data-testid="stButton"],
div[data-testid="stButton"] > button,
div[data-testid="stButton"] div[data-testid="stMarkdownContainer"],
div[data-testid="stButton"] div[data-testid="stMarkdownContainer"] p {{
    min-height: 0 !important;
}}
div[data-testid="stButton"] > button {{
    width: var(--cell-size) !important;
    height: var(--cell-size) !important;
    min-width: 0 !important;
    max-width: var(--cell-size) !important;
    max-height: var(--cell-size) !important;
    flex-shrink: 0 !important;
    flex-grow: 0 !important;
    box-sizing: border-box;
    border-radius: 8px;
    border: 1px solid {color_criteria_border};
    font-weight: 600;
    font-size: {uniform_font_size} !important;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
    line-height: 1.1;
    white-space: normal;
    word-break: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    cursor: pointer;
    transition: transform 0.1s ease, background-color 0.15s ease;
}}
div[data-testid="stButton"] > button:hover {{
    background-color: #b8cdfa;
}}
div[data-testid="stButton"] > button:active {{
    transform: scale(0.93);
}}
div[data-testid="stButton"] > button:disabled {{
    background-color: #eef0f4;
    color: #333;
    cursor: default;
    opacity: 1;
}}
{extra_css}
</style>
""", unsafe_allow_html=True)

if st.session_state.first_opening:
    welcome()
    st.session_state.first_opening = False

for row in range(5):
    cols = st.columns(4, gap="small")
    if row == 0:
        st.divider()
        if cols[0].button("**Règles**", key="menu_rules"):
            welcome()
        if cols[1].button("Générer une nouvelle grille", icon="➕", key="new_grid_reset"):
            are_you_sure("Générer une nouvelle grille", launch_new_game)
        if cols[2].button("Réinitialiser la grille", icon="🔁", key="same_grid_reset"):
            are_you_sure("Réinitialiser la grille", reload_same_game)
        if cols[3].button("Abandonner et voir les résultats", icon="❌" , key="give_up", disabled=st.session_state.end_game):
            are_you_sure("Abandonner et voir les résultats", give_up)
    else :
        for col_idx in range(4):
            i = (row-1) * 4 + col_idx
            with cols[col_idx]:
                is_clickable = (i in st.session_state.clickable_ids) | (i in criteria_ids)
                if st.button(st.session_state.labels[i], key=f"cell_{i}", disabled=not is_clickable):
                    if i in criteria_ids:
                       describe_criteria(i)
                    else :
                        if st.session_state.end_game:
                            check_answers(i)
                        else :
                            select_station(i)

err_cols = st.columns(4, gap="small")
if cols[0].button("**Erreurs**", key="errors_button", disabled=True):
    pass
errors_labels = [":x:" if st.session_state.errors > i else "" for i in range(3)]
if cols[1].button(errors_labels[0], key="1st_error", disabled=True):
    pass
if cols[2].button(errors_labels[1], key="2nd_error", disabled=True):
    pass
if cols[3].button(errors_labels[2], key="3rd_error", disabled=True):
    pass



if (len(st.session_state.user_answers) == 9) & (not st.session_state.end_game):
  st.session_state.end_game = True
  bravo()

if (st.session_state.errors == 3) & (not st.session_state.end_game):
  st.session_state.end_game = True
  you_lose()


