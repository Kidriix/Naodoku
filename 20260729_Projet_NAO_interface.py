import pandas as pd
import altair as alt
import streamlit as st
import os
import numpy as np
from datetime import datetime


st.cache_data.clear()
submitted = False

st.set_page_config(page_title="DEMO", layout="wide")

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

/* Boutons */
.stButton > button {
    background-color: #FFFFFF !important;
    color: #31333F !important;
    border: 1px solid #228B22 !important;
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

def pick_random_grid():
    a = np.random.randint(len(grids))
    selected_grid = grids.iloc[int(a)]

    return selected_grid

if "grid" not in st.session_state:
    st.session_state.grid = pick_random_grid()

def is_cell_okay(crit_col, crit_row, cell):
  crit_col_status = truth_table[truth_table["Nom arret"] == cell][crit_col].tolist()[0]
  crit_row_status = truth_table[truth_table["Nom arret"] == cell][crit_row].tolist()[0]
  if (crit_col_status == "VRAI") & (crit_row_status == "VRAI"):
     return True
  else : 
     return False
  
def is_grid_okay():
   
  for col in ["A", "B", "C"]:
    col_name = st.session_state.grid[f"Criteria {col}"]
    for row in ["D", "E", "F"]:
      row_name = st.session_state.grid[f"Criteria {row}"]
      cell = st.session_state.__getattr__(col+row)
      cell_status = is_cell_okay(col_name, row_name, cell)
      if not cell_status:
        st.session_state.grid_status = False
        st.write("Dommage, au moins 1 erreur :(")
        return
  st.session_state.grid_status = True
  st.write("Bravo !")

st.title('''
:green[**NAODOKU**]
''')
st.info('''
Bienvenue sur Naodoku, le "sudoku" Naolib !

Comment ça marche ?
- Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway et/ou Busway du réseau Naolib tout en respectant les critères de la ligne et de la colonne.
- Un arrêt ne peut être entré que dans une seule case de la grille
- La partie se termine après 3 erreurs
- Si une catégorie n'est pas claire, une petite bulle d'aide permet d'afficher une explication.

Concept calqué sur métrodoku (Lien ci-dessous) en version Nantaise.

Bon jeu !

PS : Le projet est encore *relativement* bancal et le dev du jeu n'étant pas dev de métier merci d'être indulgent :) 
''')
st.link_button(label="Lien Métrodoku", url="http://www.metrodoku.fr")

if "stations_options" not in st.session_state:
    st.session_state.stations_options = st.session_state.stations_names

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "errors" not in st.session_state:
    st.session_state.errors = 0

st.markdown("Nombre d'erreurs (max 3): ")
err_cols = st.columns(3, gap="small")
err_cols_ception = err_cols[0].columns(3, border=True, gap="small")
for i in range(st.session_state.errors):
  err_cols_ception[i].markdown(":x:")

def launch_new_game():
  st.session_state.grid = pick_random_grid()
  st.session_state.answers = {}
  st.session_state.errors = 0
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

def reload_same_game():
  st.session_state.answers = {}
  st.session_state.errors = 0
  st.session_state.stations_options = st.session_state.stations_names
  st.rerun()

@st.dialog("Choisir un arrêt")
def vote(col, row):
    crit_col = st.session_state.grid[f"Criteria {col}"]
    crit_row = st.session_state.grid[f"Criteria {row}"]
    st.markdown(f"Sélectionner un arrêt vérifiant **{crit_col}** et **{crit_row}**")
    station = st.selectbox(label=f"{st.session_state.grid[f"Stations {col+row}"]} arrêts possibles", options=st.session_state.stations_options, key=col+row)
    stop_cols = st.columns(2)
    if stop_cols[0].button("Valider", type="primary", key=f"valider_{col+row}"):
      if station == " ":
        st.warning("Aucun arrêt sélectionné")
      else:
        if is_cell_okay(crit_col, crit_row, station):
            st.session_state.answers[col+row] = station
            st.session_state.stations_options.remove(station)
        else :
            st.session_state.errors += 1
        st.rerun()
    if stop_cols[1].button("Annuler", key=f"annuler_{col+row}"):
      st.session_state.__delattr__(col+row)
      st.rerun()

@st.dialog("Bravo !")
def bravo():
  st.balloons()
  st.markdown('''
  Grille complète, bravo !
  ''')
  win_cols = st.columns(2)
  if win_cols[0].button("Nouvelle grille", key="new_grid_replay_win"):
    launch_new_game()
  if win_cols[1].button("Rejouer la grille", key="same_grid_replay_win"):
    reload_same_game()

@st.dialog("Dommage...")
def you_lose():
  st.markdown('''
  Dommage : 3 erreurs, c'est perdu
  ''')
  lose_cols = st.columns(2)
  if lose_cols[0].button("Nouvelle grille", key="new_grid_replay_lose"):
    launch_new_game()
  if lose_cols[1].button("Rejouer la grille", key="same_grid_replay_lose"):
    reload_same_game()
  

for row in range(4):
  grid_cols = st.columns(4, border=True)
  if row == 0:
    with grid_cols[1].container():
      st.markdown(f"**{st.session_state.grid["Criteria A"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria A"]]["Description"].tolist()[0])
    grid_cols[2].markdown(f"**{st.session_state.grid["Criteria B"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria B"]]["Description"].tolist()[0])
    grid_cols[3].markdown(f"**{st.session_state.grid["Criteria C"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria C"]]["Description"].tolist()[0])
  elif row == 1:
    grid_cols[0].markdown(f"**{st.session_state.grid["Criteria D"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria D"]]["Description"].tolist()[0])
    
    if "AD" not in st.session_state.answers:
      AD_button = grid_cols[1].button(label=f"{st.session_state.grid[f"Stations AD"]} arrêts possibles", key="AD_button", on_click=vote, kwargs={"col":"A", "row":"D"})
    else : 
      grid_cols[1].markdown(st.session_state.answers["AD"])

    if "BD" not in st.session_state.answers:
      BD_button = grid_cols[2].button(label=f"{st.session_state.grid[f"Stations BD"]} arrêts possibles", key="BD_button", on_click=vote, kwargs={"col":"B", "row":"D"})
    else : 
      grid_cols[2].write(st.session_state.answers["BD"])

    if "CD" not in st.session_state.answers:
      CD_button = grid_cols[3].button(label=f"{st.session_state.grid[f"Stations CD"]} arrêts possibles", key="CD_button", on_click=vote, kwargs={"col":"C", "row":"D"})
    else : 
      grid_cols[3].write(st.session_state.answers["CD"])

  elif row == 2:
    grid_cols[0].markdown(f"**{st.session_state.grid["Criteria E"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria E"]]["Description"].tolist()[0])
    if "AE" not in st.session_state.answers:
      AE_button = grid_cols[1].button(label=f"{st.session_state.grid[f"Stations AE"]} arrêts possibles", key="AE_button", on_click=vote, kwargs={"col":"A", "row":"E"})
    else : 
      grid_cols[1].markdown(st.session_state.answers["AE"])

    if "BE" not in st.session_state.answers:
      BE_button = grid_cols[2].button(label=f"{st.session_state.grid[f"Stations BE"]} arrêts possibles", key="BE_button", on_click=vote, kwargs={"col":"B", "row":"E"})
    else : 
      grid_cols[2].write(st.session_state.answers["BE"])

    if "CE" not in st.session_state.answers:
      CE_button = grid_cols[3].button(label=f"{st.session_state.grid[f"Stations CE"]} arrêts possibles", key="CE_button", on_click=vote, kwargs={"col":"C", "row":"E"})
    else : 
      grid_cols[3].write(st.session_state.answers["CE"])

  elif row == 3:
    grid_cols[0].markdown(f"**{st.session_state.grid["Criteria F"]}**", help=legend[legend["Nom critere"]==st.session_state.grid["Criteria F"]]["Description"].tolist()[0])
    if "AF" not in st.session_state.answers:
      AF_button = grid_cols[1].button(label=f"{st.session_state.grid[f"Stations AF"]} arrêts possibles", key="AF_button", on_click=vote, kwargs={"col":"A", "row":"F"})
    else : 
      grid_cols[1].markdown(st.session_state.answers["AF"])

    if "BF" not in st.session_state.answers:
      BF_button = grid_cols[2].button(label=f"{st.session_state.grid[f"Stations BF"]} arrêts possibles", key="BF_button", on_click=vote, kwargs={"col":"B", "row":"F"})
    else : 
      grid_cols[2].write(st.session_state.answers["BF"])

    if "CF" not in st.session_state.answers:
      CF_button = grid_cols[3].button(label=f"{st.session_state.grid[f"Stations CF"]} arrêts possibles", key="CF_button", on_click=vote, kwargs={"col":"C", "row":"F"})
    else : 
      grid_cols[3].write(st.session_state.answers["CF"])

if len(st.session_state.answers) == 9:
  bravo()

if st.session_state.errors == 3:
  you_lose()

with st.sidebar:
  st.title("C'est le menu")
  if st.button("Nouvelle grille", key="new_grid_reset"):
      launch_new_game()
  if st.button("Réinitialiser la grille", key="same_grid_reset"):
      reload_same_game()
  
# ---- OLD VERSION ------
# with st.form("Main Form"):
#   st.write("Nouvelle partie de NAODOKU !")

#   stations_options = st.session_state.stations_names

#   for row in range(4):
#     cols = st.columns([0.25, 0.25, 0.25, 0.25])
#     if row == 0:
#       cols[1].markdown(st.session_state.grid["Criteria A"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria A"]]["Description"].tolist()[0])
#       cols[2].markdown(st.session_state.grid["Criteria B"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria B"]]["Description"].tolist()[0])
#       cols[3].markdown(st.session_state.grid["Criteria C"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria C"]]["Description"].tolist()[0])
#     elif row == 1:
#       cols[0].markdown(st.session_state.grid["Criteria D"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria D"]]["Description"].tolist()[0])
#       AD = cols[1].selectbox(label=f"{st.session_state.grid["Stations AD"]} arrêts possibles", options=stations_options, key="AD")
#       BD = cols[2].selectbox(label=f"{st.session_state.grid["Stations BD"]} arrêts possibles", options=stations_options, key="BD")
#       CD = cols[3].selectbox(label=f"{st.session_state.grid["Stations CD"]} arrêts possibles", options=stations_options, key="CD")
#     elif row == 2:
#       cols[0].markdown(st.session_state.grid["Criteria E"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria E"]]["Description"].tolist()[0])
#       AE = cols[1].selectbox(label=f"{st.session_state.grid["Stations AE"]} arrêts possibles", options=stations_options, key="AE")
#       BE = cols[2].selectbox(label=f"{st.session_state.grid["Stations BE"]} arrêts possibles", options=stations_options, key="BE")
#       CE = cols[3].selectbox(label=f"{st.session_state.grid["Stations CE"]} arrêts possibles", options=stations_options, key="CE")
#     elif row == 3:
#       cols[0].markdown(st.session_state.grid["Criteria F"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria F"]]["Description"].tolist()[0])
#       AF = cols[1].selectbox(label=f"{st.session_state.grid["Stations AF"]} arrêts possibles", options=stations_options, key="AF")
#       BF = cols[2].selectbox(label=f"{st.session_state.grid["Stations BF"]} arrêts possibles", options=stations_options, key="BF")
#       CF = cols[3].selectbox(label=f"{st.session_state.grid["Stations CF"]} arrêts possibles", options=stations_options, key="CF")

#   submitted = st.form_submit_button(label="Vérifier la grille")
#   if submitted :
#     is_grid_okay()
