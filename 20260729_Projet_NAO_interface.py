import random
import streamlit as st
import pandas as pd
import altair as alt
import time
import numpy as np
import os
from datetime import datetime
import base64
import requests

from core.airtable import *
from core.dialogs import *
from core.interface_utils import *
from core.utils import *

from constants.ref_files_paths import *
from constants.dict_lists_setup import *
from constants.texts import *
from constants.svg_images import *
from constants.css_setup import *

max_errors = 3

st.session_state.stations_names = stations_names

if "first_opening" not in st.session_state:
    st.session_state.first_opening = True

if "grid" not in st.session_state:
    st.session_state.grid = pick_random_grid()
    st.session_state.grid_difficulty = float(st.session_state.grid["Score"])

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
    st.session_state.clickable_ids = clickable_ids.copy()

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False

if "grid_difficulty" not in st.session_state:
    st.session_state.grid_difficulty = 0

if "game_start_time" not in st.session_state:
    st.session_state.game_start_time = time.time()

if "logo_svg_b64" not in st.session_state:
    random_bus_tram_logo()

if "nb_hints_left" not in st.session_state:
   st.session_state.nb_hints_left = 3

if "hint1_active" not in st.session_state:
   st.session_state.hint1_active = default_hints_state.copy()

if "hint2_active" not in st.session_state:
   st.session_state.hint2_active = default_hints_state.copy()

if "hint3_active" not in st.session_state:
   st.session_state.hint3_active = default_hints_state.copy()

def launch_new_game(difficulty=None):
  st.session_state.grid = pick_random_grid(difficulty)
  st.session_state.grid_difficulty = float(st.session_state.grid["Score"])
  st.session_state.end_game = False
  st.session_state.user_answers = {}
  st.session_state.grid_answers = get_grid_possibilities(st.session_state.grid)
  st.session_state.errors = 0
  st.session_state.clickable_ids = clickable_ids.copy()
  st.session_state.stations_options = st.session_state.stations_names
  st.session_state.game_duration = 0
  st.session_state.game_start_time = time.time()
  st.session_state.result_saved = False
  st.session_state.nb_hints_left = 3
  st.session_state.hint1_active = default_hints_state.copy()
  st.session_state.hint2_active = default_hints_state.copy()
  st.session_state.hint3_active = default_hints_state.copy()
  random_bus_tram_logo()
  st.rerun()

def reload_same_game():
  st.session_state.user_answers = {}
  st.session_state.errors = 0
  st.session_state.end_game = False
  st.session_state.clickable_ids = clickable_ids.copy()
  st.session_state.stations_options = st.session_state.stations_names
  st.session_state.game_duration = 0
  st.session_state.game_start_time = time.time()
  st.session_state.result_saved = False
  st.session_state.nb_hints_left = 3
  st.session_state.hint1_active = default_hints_state.copy()
  st.session_state.hint2_active = default_hints_state.copy()
  st.session_state.hint3_active = default_hints_state.copy()
  random_bus_tram_logo()
  st.rerun()

def give_up():
  st.session_state.end_game = True
  st.session_state.clickable_ids = clickable_ids.copy()
  st.rerun()

def save_result_airtable(grid, user_answers, duration):
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

def save_game_stats(grid, user_answers, duration):
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

def is_hint_used_in_grid(hint_number):
   # Checks if hint no i has already been used in the grid 
   hint_status = st.session_state.__getattr__(f"hint{hint_number}_active")
   return np.any(list(hint_status.values()))

def is_a_hint_used_in_cell(col, row):
   res = False
   for hint_idx in range(1, 4):
      res |= st.session_state.__getattr__(f"hint{hint_idx}_active")[col+row]
   return res

@st.dialog("Choisir un arrêt")
def select_station(cell_id):
    col, row = grid_ids_to_letters[cell_id][0], grid_ids_to_letters[cell_id][1]
    crit_col = st.session_state.grid[f"Criteria {col}"]
    crit_row = st.session_state.grid[f"Criteria {row}"]
    st.markdown(f"Sélectionner un arrêt vérifiant **{crit_col}** et **{crit_row}**")
    if len(st.session_state.grid_answers[col+row]) <= 5:
        hint_expander = st.expander(f"Utiliser un indice ? ({st.session_state.nb_hints_left} restants)")
        hint_tabs = hint_expander.tabs(["Première lettre", "Ligne", "QCM"])
        
        hint_tabs[0].markdown(''' 
            Première lettre et nombre de lettres de chacune des solutions :
        ''')
        if hint_tabs[0].button("Utiliser l'indice", key="hint1_button"+col+row, disabled=((st.session_state.nb_hints_left <= 0) | (is_a_hint_used_in_cell(col, row)) | is_hint_used_in_grid(1))):
            st.session_state.nb_hints_left -= 1
            st.session_state.hint1_active[col+row] = True
        if st.session_state.hint1_active[col+row] == True :
            for (i,station) in enumerate(st.session_state.grid_answers[col+row]):
                with hint_tabs[0].container(border=True, key="hint1_container_"+col+row+str(i)):
                    st.markdown(convert_word_to_dashes(station))

        hint_tabs[1].markdown(''' 
            Lignes disponibles pour chacune des solutions :
        ''')
        if hint_tabs[1].button("Utiliser l'indice", key="hint2_button"+col+row, disabled=((st.session_state.nb_hints_left <= 0) | (is_a_hint_used_in_cell(col, row)) | is_hint_used_in_grid(2))):
            st.session_state.nb_hints_left -= 1
            st.session_state.hint2_active[col+row] = True
        if st.session_state.hint2_active[col+row] == True :
            for (i,station) in enumerate(st.session_state.grid_answers[col+row]):
                with hint_tabs[1].container(border=True, key="hint2_container_"+col+row+str(i)):
                    show_logo(get_lines_from_station(station))
        
        hint_tabs[2].markdown(''' 
            1 seul arrêt correct parmi 4 au choix :
        ''')
        hint_mcq_list = multiple_choice_question(col+row, st.session_state.grid_answers, st.session_state.user_answers, st.session_state.stations_options)
        if hint_tabs[2].button("Utiliser l'indice", key="hint3_button"+col+row, disabled=((st.session_state.nb_hints_left <= 0) | (is_a_hint_used_in_cell(col, row)) | is_hint_used_in_grid(3))):
            st.session_state.nb_hints_left -= 1
            st.session_state.hint3_active[col+row] = True
        if st.session_state.hint3_active[col+row] == True :
            for (i,station) in enumerate(hint_mcq_list):
                with hint_tabs[2].container(border=True, key="hint3_container_"+col+row+str(i)):
                    st.markdown(station)
        
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
  st.session_state.clickable_ids = clickable_ids.copy()
  st.markdown(f'''
  Grille complétée en **{time.gmtime(st.session_state.game_duration).tm_min} min** et **{time.gmtime(st.session_state.game_duration).tm_sec} s**
  **Nombre d'indices utilisés** : {3-st.session_state.nb_hints_left}
  Bravo !
  
  ''')
  win_cols = st.columns(4)
  if win_cols[0].button("Nouvelle grille", key="new_grid_replay_win", type="primary"):
    launch_new_game()
  if win_cols[1].button("Rejouer la grille", key="same_grid_replay_win"):
    reload_same_game()
  if win_cols[2].button("Voir les solutions", key="check_answers_win"):
    st.session_state.clickable_ids = clickable_ids.copy()
    st.rerun()
  if win_cols[3].button("Ballons :)", key="balloons_win"):
    st.balloons()

@st.dialog("Dommage...")
def you_lose():
  st.markdown(you_lose_text)
  lose_cols = st.columns(3)
  if lose_cols[0].button("Nouvelle grille", key="new_grid_replay_lose"):
    launch_new_game()
  if lose_cols[1].button("Rejouer la grille", key="same_grid_replay_lose"):
    reload_same_game()
  if lose_cols[2].button("Voir les solutions", key="check_answers_lose"):
    st.session_state.clickable_ids = clickable_ids.copy()
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

@st.dialog("Nouvelle Grille")
def select_difficulty():
   st.markdown('''
    Choisir un niveau de difficulté 
    - Facile : De 1 à 2/5
    - Normal : De 2,5 à 3,5/5 
    - Difficile : De 4 à 5/5          
    ''')
   difficulty_level = st.selectbox("Niveau de difficulté pour la nouvelle grille", ["Facile", "Normal", "Difficile"], key = "difficulty_choice", help=difficulty_explanation)
   difficulty_choice = difficulty_FR_EN[difficulty_level]
   confirm_cols = st.columns(2)
   if confirm_cols[0].button("Confirmer", key=f"confirm_difficulty", type="primary"):
    launch_new_game(difficulty_choice)
   if confirm_cols[1].button("Annuler", key=f"cancel_difficulty"):
    st.rerun()

st.session_state.labels = generate_labels(st.session_state.grid, st.session_state.user_answers, st.session_state.grid_answers, st.session_state.end_game)

uniform_font_size = set_font_size(st.session_state.labels)

cells_colors_css = set_cells_colors(st.session_state.user_answers)
extra_css += cells_colors_css
     
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

# sb = st.sidebar
# sb.markdown("Menu")
# if sb.button("**Règles**", key="menu_rules_sb"):
#     welcome()
# if sb.button("Générer une nouvelle grille", icon="➕", key="new_grid_reset_sb"):
#     select_difficulty()
# if sb.button("Réinitialiser la grille", icon="🔁", key="same_grid_reset_sb"):
#     are_you_sure("Réinitialiser la grille", reload_same_game)
# if sb.button("Abandonner et voir les résultats", icon="❌" , key="give_up_sb", disabled=st.session_state.end_game):
#     are_you_sure("Abandonner et voir les résultats", give_up)

if st.session_state.first_opening:
    welcome()
    st.session_state.first_opening = False

st.image(os.path.join(WK_FOLDER, ".images", "naodoku.png"))

for row in range(5):
    cols = st.columns(4, gap="small")
    if row == 0:
        menu_expander = st.expander("**Menu**", icon="⚙️")
        menu_cols = menu_expander.columns(4, gap="small")
        if menu_cols[0].button("**Règles et Indices**", key="menu_rules"):
            welcome(explain_hints=True)
        if menu_cols[1].button("Nouvelle grille", key="new_grid_reset"):
            select_difficulty()
        if menu_cols[2].button("Réinitialiser la grille", key="same_grid_reset"):
            are_you_sure("Réinitialiser la grille", reload_same_game)
        if menu_cols[3].button("Abandonner et voir les résultats", key="give_up", disabled=st.session_state.end_game):
            are_you_sure("Abandonner et voir les résultats", give_up)
        
        metrics_container = st.container()
        metrics_cols = metrics_container.columns(2)
        metrics_cols[0].markdown(f'''**Difficulté :** {st.session_state.grid_difficulty} / 5''')
        metrics_cols[1].markdown(f'''**Indices :** {st.session_state.nb_hints_left} / 3''')
        st.divider()
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

def switch_to_endgame_mode():
    st.session_state.end_game = True
    st.session_state.game_duration = time.time() - st.session_state.game_start_time
    if not st.session_state.get("result_saved", False):
        save_result_airtable(st.session_state.grid, st.session_state.user_answers, st.session_state.game_duration)
        st.session_state.result_saved = True


if (len(st.session_state.user_answers) == 9) & (not st.session_state.end_game):
  switch_to_endgame_mode()
  bravo()

if (st.session_state.errors == max_errors) & (not st.session_state.end_game):
  switch_to_endgame_mode()
  you_lose()
