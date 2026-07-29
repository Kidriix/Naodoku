import pandas as pd
import altair as alt
import streamlit as st
import os
import numpy as np
from datetime import datetime

st.cache_data.clear()
submitted = False

st.set_page_config(page_title="DEMO", layout="wide")

refresh = False
grids = pd.read_csv("20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv("20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv("20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')

stations_names = [" "] + truth_table["Nom arret"].tolist()
st.session_state.stations_names = stations_names

def pick_random_grid():
    a = np.random.randint(len(grids))
    selected_grid = grids.iloc[int(a)]

    # transpose = np.random.randint(2)
    # if transpose == 1:
    #   selected_grid.swaplevel(1,4)
    #   selected_grid.swaplevel(2,5)
    #   selected_grid.swaplevel(3,6)

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

def update_stations_list():
  for col in ["A", "B", "C"]:
    for row in ["D", "E", "F"]:
      cell = st.session_state.__getattr__(col+row)
      if cell != " ":
        stations_options.remove(cell)
  return stations_options

with st.form("Nouvelle partie de NAODOKU !"):
  st.write("Nouvelle partie de NAODOKU !")

  stations_options = st.session_state.stations_names

  for row in range(4):
    cols = st.columns(4)
    if row == 0:
      cols[1].markdown(st.session_state.grid["Criteria A"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria A"]]["Description"].tolist()[0])
      cols[2].markdown(st.session_state.grid["Criteria B"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria B"]]["Description"].tolist()[0])
      cols[3].markdown(st.session_state.grid["Criteria C"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria C"]]["Description"].tolist()[0])
    elif row == 1:
      cols[0].markdown(st.session_state.grid["Criteria D"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria D"]]["Description"].tolist()[0])
      AD = cols[1].selectbox(label=f"{st.session_state.grid["Stations AD"]} arrêts possibles", options=stations_options, key="AD")
      BD = cols[2].selectbox(label=f"{st.session_state.grid["Stations BD"]} arrêts possibles", options=stations_options, key="BD")
      CD = cols[3].selectbox(label=f"{st.session_state.grid["Stations CD"]} arrêts possibles", options=stations_options, key="CD")
    elif row == 2:
      cols[0].markdown(st.session_state.grid["Criteria E"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria E"]]["Description"].tolist()[0])
      AE = cols[1].selectbox(label=f"{st.session_state.grid["Stations AE"]} arrêts possibles", options=stations_options, key="AE")
      BE = cols[2].selectbox(label=f"{st.session_state.grid["Stations BE"]} arrêts possibles", options=stations_options, key="BE")
      CE = cols[3].selectbox(label=f"{st.session_state.grid["Stations CE"]} arrêts possibles", options=stations_options, key="CE")
    elif row == 3:
      cols[0].markdown(st.session_state.grid["Criteria F"], help=legend[legend["Nom critere"]==st.session_state.grid["Criteria F"]]["Description"].tolist()[0])
      AF = cols[1].selectbox(label=f"{st.session_state.grid["Stations AF"]} arrêts possibles", options=stations_options, key="AF")
      BF = cols[2].selectbox(label=f"{st.session_state.grid["Stations BF"]} arrêts possibles", options=stations_options, key="BF")
      CF = cols[3].selectbox(label=f"{st.session_state.grid["Stations CF"]} arrêts possibles", options=stations_options, key="CF")

  submitted = st.form_submit_button(label="Vérifier la grille")
  if submitted :
    is_grid_okay()

if st.button("Nouvelle grille"):
    st.session_state.grid = pick_random_grid()
    st.rerun()
