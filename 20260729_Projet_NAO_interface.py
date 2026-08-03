import streamlit as st
import pandas as pd
import altair as alt
import time
import numpy as np
import os
from datetime import datetime
import base64
import requests

def get_airtable_headers():
    return {
        "Authorization": f"Bearer {st.secrets['airtable']['token']}",
        "Content-Type": "application/json"
    }

def get_airtable_url():
    base_id = st.secrets["airtable"]["base_id"]
    table = st.secrets["airtable"]["table_name"]
    return f"https://api.airtable.com/v0/{base_id}/{table}"


def get_all_results():
    all_records = []
    url = get_airtable_url()
    params = {}
    while True:
        response = requests.get(url, headers=get_airtable_headers(), params=params)
        result = response.json()
        all_records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break
        params["offset"] = offset
    return pd.DataFrame([r["fields"] for r in all_records])

st.set_page_config(page_title="NAO_DEMO", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

grids = pd.read_csv("20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv("20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv("20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')
stats_save_file = os.path.join(BASE_DIR, ".stats", "Projet_NAO_stats.csv")

lines_logos = [
    os.path.join(BASE_DIR, ".images", f"indices de ligne_svg_picto ligne {i}.svg")
    for i in range(1, 6)
]

TRAM_SVG = '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M18.9679 16.7134L18.1211 8.57285C18.1211 8.56462 18.1203 8.55722 18.1195 8.54899L18.0652 8.02724C17.8602 6.05876 16.1238 4.57417 14.0261 4.57417H12.9226L14.2376 2.82459H15.4194V3.2591H16.2423V2.41229C16.2423 2.18434 16.058 2 15.8309 2H9.16831C8.94118 2 8.75684 2.18434 8.75684 2.41229V3.2591H9.57979V2.82459H10.7615L12.0766 4.57417H10.9582C8.86053 4.57417 7.12412 6.05876 6.91921 8.02724L6.01562 16.7134C5.9325 17.5092 6.18843 18.2819 6.73487 18.8901C7.2525 19.4653 7.97916 19.8233 8.76425 19.8998L7.3743 22H9.0531L9.47116 21.368H15.6737L16.0917 22H17.7705L16.3691 19.8817C17.0966 19.7772 17.7648 19.4291 18.2495 18.8901C18.7959 18.2819 19.051 17.5092 18.9679 16.7134ZM11.689 2.82459H13.3094L12.4988 3.90265L11.689 2.82459ZM8.25567 8.69876L8.31081 8.1729C8.44083 6.92038 9.57979 5.97646 10.9582 5.97646H14.0253C15.4046 5.97646 16.5427 6.92038 16.6727 8.1729L16.7287 8.70699C16.825 9.76777 16.4736 10.7981 15.7371 11.6112C14.9273 12.5049 13.7447 13.0176 12.493 13.0176C11.2413 13.0176 10.0637 12.5073 9.2539 11.6169C8.51243 10.8014 8.15856 9.7653 8.25732 8.69876H8.25567ZM10.0168 20.5434L10.4324 19.9155H14.7125L15.1281 20.5434H10.0168ZM17.2101 17.9519C16.8892 18.3091 16.4127 18.514 15.9041 18.514H9.07944C8.57086 18.514 8.0952 18.3091 7.77342 17.9519C7.49527 17.6425 7.36524 17.2549 7.40639 16.8591L7.8944 12.1675C7.99562 12.3024 8.10342 12.4333 8.21946 12.5608C9.29422 13.7418 10.8512 14.419 12.4922 14.419C14.1331 14.419 15.6975 13.7385 16.7723 12.5526C16.8851 12.4283 16.9896 12.3 17.0883 12.1691L17.5763 16.8591C17.6175 17.2549 17.4883 17.6425 17.2101 17.9519Z" fill="#000000"/>
<path d="M10.0011 15.2914C9.4835 15.2914 9.06462 15.7119 9.06462 16.2295C9.06462 16.7472 9.48432 17.1677 10.0011 17.1677C10.5179 17.1677 10.9376 16.748 10.9376 16.2295C10.9376 15.7111 10.5179 15.2914 10.0011 15.2914Z" fill="#000000"/>
<path d="M14.9972 15.2914C14.4796 15.2914 14.0607 15.7119 14.0607 16.2295C14.0607 16.7472 14.4804 17.1677 14.9972 17.1677C15.514 17.1677 15.9337 16.748 15.9337 16.2295C15.9337 15.7111 15.514 15.2914 14.9972 15.2914Z" fill="#000000"/>
</svg>'''

BUS_SVG = '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M8.24995 15.3799C7.73426 15.3799 7.31645 15.8018 7.31645 16.3225C7.31645 16.8431 7.73426 17.265 8.24995 17.265C8.76564 17.265 9.18345 16.8431 9.18345 16.3225C9.18345 15.8018 8.76564 15.3799 8.24995 15.3799Z" fill="#000000"/>
<path d="M15.7501 15.3799C15.2344 15.3799 14.8165 15.8018 14.8165 16.3225C14.8165 16.8431 15.2344 17.265 15.7501 17.265C16.2657 17.265 16.6836 16.8431 16.6836 16.3225C16.6836 15.8018 16.2657 15.3799 15.7501 15.3799Z" fill="#000000"/>
<path d="M21.3001 6.40594H20.184V5.47244C20.1823 3.55773 18.6353 1.99915 16.7345 1.99915H7.2671C5.36555 1.99997 3.81766 3.55773 3.81684 5.47326V6.40676H2.69992C2.31336 6.40676 2 6.72012 2 7.10586V8.99836C2 9.38492 2.31336 9.69746 2.69992 9.69746H3.81437L3.81026 16.6704C3.81026 17.5973 4.16721 18.4699 4.81696 19.1263C5.07275 19.3845 5.36143 19.5959 5.67315 19.7596V21.3C5.67315 21.6866 5.98651 21.9991 6.37307 21.9991H7.30493C7.69149 21.9991 8.00485 21.6858 8.00485 21.3V20.1469H15.9943V21.3C15.9943 21.6866 16.3077 21.9991 16.6942 21.9991H17.6261C18.0127 21.9991 18.326 21.6858 18.326 21.3V19.7596C18.6377 19.5967 18.9273 19.3845 19.1822 19.1263C19.832 18.4699 20.1897 17.5973 20.1889 16.6704L20.1848 9.69746H21.2993C21.6858 9.69746 21.9992 9.3841 21.9992 8.99836V7.10586C21.9992 6.7193 21.6858 6.40676 21.2993 6.40676L21.3001 6.40594ZM7.26627 3.39817H16.7337C17.863 3.39817 18.7825 4.3292 18.7833 5.47326L18.785 8.4029C18.6879 9.68595 18.0357 10.6458 16.7962 11.3292C15.6193 11.9774 13.9159 12.3351 11.9996 12.3351C10.0832 12.3351 8.3799 11.9782 7.20294 11.3292C5.96348 10.6466 5.31126 9.68595 5.21421 8.4029L5.21586 5.47408C5.21586 4.33003 6.1362 3.39899 7.26545 3.39899L7.26627 3.39817ZM18.1879 18.1434C17.8013 18.5341 17.2872 18.7496 16.7403 18.7496H7.2597C6.71357 18.7496 6.19953 18.5341 5.81215 18.1434C5.42312 17.7503 5.20928 17.228 5.2101 16.6712L5.21339 11.5809C5.58268 11.9486 6.02106 12.2743 6.52852 12.5539C8.29765 13.5285 10.4805 13.7333 12.0004 13.7333C13.5203 13.7333 15.7032 13.5285 17.4723 12.5539C17.9798 12.2743 18.4181 11.9486 18.7874 11.5809L18.7907 16.6712C18.7907 17.2272 18.5761 17.7503 18.1879 18.1434Z" fill="#000000"/>
</svg>'''

max_errors = 3

stations_names = [" "] + sorted(truth_table["Nom arret"].tolist())
st.session_state.stations_names = stations_names
row_letters = ["D", "E", "F"]
col_letters = ["A", "B", "C"]

clickable_ids = {5, 6, 7, 9, 10, 11, 13, 14, 15}  # exemple : 9 cases cliquables
criteria_ids = {1, 2, 3, 4, 8, 12}
grid_ids_to_letters = {1:"A", 2:"B", 3:"C", 4:"D", 5:"AD", 6:"BD", 7:"CD", 8:"E", 9:"AE", 10:"BE", 11:"CE", 12:"F", 13:"AF", 14:"BF", 15:"CF"}

if "first_opening" not in st.session_state:
    st.session_state.first_opening = True

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

def show_logo(line_id):
   path_logo = f"images\\indices de ligne_svg_picto ligne {line_id}.svg"
   st.image(path_logo)

def random_bus_tram_logo():
    st.session_state.chosen_svg = TRAM_SVG if np.random.rand() < 0.5 else BUS_SVG
    st.session_state.logo_svg_b64 = base64.b64encode(st.session_state.chosen_svg.encode("utf-8")).decode("utf-8")

def switch_bus_tram_logo():
    if st.session_state.chosen_svg == TRAM_SVG:
      st.session_state.chosen_svg = BUS_SVG
    else : 
      st.session_state.chosen_svg = TRAM_SVG
    st.session_state.logo_svg_b64 = base64.b64encode(st.session_state.chosen_svg.encode("utf-8")).decode("utf-8")

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

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "game_start_time" not in st.session_state:
    st.session_state.game_start_time = time.time()

if "logo_svg_b64" not in st.session_state:
    random_bus_tram_logo()

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
  st.session_state.game_duration = 0
  st.session_state.game_start_time = time.time()
  st.session_state.result_saved = False
  random_bus_tram_logo()
  st.rerun()

def reload_same_game():
  st.session_state.user_answers = {}
  st.session_state.errors = 0
  st.session_state.end_game = False
  st.session_state.clickable_ids = clickable_ids
  st.session_state.stations_options = st.session_state.stations_names
  st.session_state.game_duration = 0
  st.session_state.game_start_time = time.time()
  st.session_state.result_saved = False
  random_bus_tram_logo()
  st.rerun()

def give_up():
  st.session_state.end_game = True
  st.rerun()

def save_result_airtable():
    try:
        stats = {}
        for letter_id in col_letters + row_letters:
            stats[f"Critere {letter_id}"] = st.session_state.grid[f"Criteria {letter_id}"]
        for col_id in col_letters:
            for row_id in row_letters:
                if col_id+row_id in st.session_state.user_answers:
                    stats[f"Arret {col_id+row_id}"] = st.session_state.user_answers[col_id+row_id]
                else : 
                    stats[f"Arret {col_id+row_id}"] = "Non renseigné"
        stats["Temps"] = str(st.session_state.game_duration)
        
        data = {
            "fields": stats
        }

        response = requests.post(get_airtable_url(), headers=get_airtable_headers(), json=data, timeout=5)
        if response.status_code != 200:
            st.toast("⚠️ Le résultat n'a pas pu être enregistré.", icon="⚠️")
        return response.status_code == 200
    except Exception as e:
        st.toast("⚠️ Le résultat n'a pas pu être enregistré.", icon="⚠️")
        return False

def save_game_stats():
    stats = {}
    for letter_id in col_letters + row_letters:
       stats[f"Critere {letter_id}"] = st.session_state.grid[f"Criteria {letter_id}"]
    for col_id in col_letters:
       for row_id in row_letters:
          stats[f"Arret {col_id+row_id}"] = st.session_state.user_answers[col_id+row_id]
    
    stats["Temps"] = str(st.session_state.game_duration)
    
    stats_cols = [f"Critere {i}" for i in col_letters+row_letters] + [f"Arret {col_id+row_id}" for col_id in col_letters for row_id in row_letters] + ["Temps"]
    
    stats_df = pd.DataFrame([stats], columns=stats_cols, dtype=str)
    
    stats_df.to_csv(stats_save_file, sep=";", mode="a", encoding="utf-8", header=False, index=False)

@st.dialog("Bienvenue")
def welcome():
    
    st.markdown(f'''
        Bienvenue sur Naodoku, le "sudoku" Naolib !

        Comment ça marche ?
        - Le but du jeu est de remplir les 9 cases de la grille avec des arrêts de Tramway (Lignes 1, 2 et 3) et/ou Busway (Lignes 4 et 5) du réseau Naolib.''')
    st.image(lines_logos)

    st.markdown('''
        - Un arrêt est valide dans une case si il respecte à la fois les critères de la ligne et de la colonne.
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
   crit = st.session_state.grid[f"Criteria {grid_ids_to_letters[cell_id]}"]
   desc = legend[legend["Nom critere"]==st.session_state.grid[f"Criteria {grid_ids_to_letters[cell_id]}"]]["Description"].tolist()[0]
   st.title(f"**{crit}**")
   st.markdown(desc)

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
  st.session_state.clickable_ids = clickable_ids
  st.markdown(f'''
  Grille complétée en **{time.gmtime(st.session_state.game_duration).tm_min} min** et **{time.gmtime(st.session_state.game_duration).tm_sec} s** bravo !
  
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

# --- Config des 16 cases : lesquelles sont cliquables ---

labels = []
for i in range(16):
    if i == 0:
        labels.append("**NAODOKU**")
    elif len(grid_ids_to_letters[i]) == 1:
        labels.append(f"**{st.session_state.grid[f"Criteria {grid_ids_to_letters[i]}"]}**")
    elif grid_ids_to_letters[i] in st.session_state.user_answers :
        labels.append(st.session_state.user_answers[grid_ids_to_letters[i]])
    elif st.session_state.end_game : 
        labels.append(f"Voir les {len(st.session_state.grid_answers[grid_ids_to_letters[i]])} solutions")
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
[data-testid="stHorizontalBlock"] {{
    max-width: 480px;
    margin: 0 auto;
    flex-wrap: nowrap !important;
    flex-direction: row !important;
    gap: min(2vw, 10px) !important;
}}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
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
.st-key-cell_0 button {{
    background-image: url("data:image/svg+xml;base64,{st.session_state.logo_svg_b64}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 55% 55% !important;
}}
.st-key-cell_0 button * {{
    font-size: 0 !important;
    color: transparent !important;
    line-height: 0 !important;
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
                is_clickable = (i in st.session_state.clickable_ids) | (i in criteria_ids) | (i == 0)
                if st.button(st.session_state.labels[i], key=f"cell_{i}", disabled=not is_clickable):
                    if i in criteria_ids:
                       describe_criteria(i)
                    elif i == 0:
                       switch_bus_tram_logo()
                    else :
                        if st.session_state.end_game:
                            check_answers(i)
                        else :
                            select_station(i)

err_cols = st.columns(max_errors +1, gap="small")
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
  st.session_state.game_duration = time.time() - st.session_state.game_start_time
  if not st.session_state.get("result_saved", False):
    save_result_airtable()
    st.session_state.result_saved = True
  bravo()

if (st.session_state.errors == max_errors) & (not st.session_state.end_game):
  st.session_state.end_game = True
  st.session_state.game_duration = time.time() - st.session_state.game_start_time
  if not st.session_state.get("result_saved", False):
    save_result_airtable()
    st.session_state.result_saved = True
  you_lose()
