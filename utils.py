import numpy as np
import pandas as pd
import streamlit as st
from constants.dict_lists_setup import *
import random
from constants.ref_files_paths import *

# ------------------ Grid setup --------------------------
def pick_random_grid(difficulty=None):
    if difficulty is not None:
      min_bound, up_bound = difficulty_bounds[difficulty]["min"], difficulty_bounds[difficulty]["max"]
      filtered_grids = grids[(grids["Score"] >= min_bound) & (grids["Score"] <= up_bound)]
    else : 
      filtered_grids = grids
    a = np.random.randint(len(filtered_grids))
    selected_grid = filtered_grids.iloc[int(a)]

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

def is_cell_okay(crit_col, crit_row, cell):
  crit_col_status = truth_table[truth_table["Nom arret"] == cell][crit_col].tolist()[0]
  crit_row_status = truth_table[truth_table["Nom arret"] == cell][crit_row].tolist()[0]
  if (crit_col_status == "VRAI") & (crit_row_status == "VRAI"):
     return True
  else : 
     return False
  
def generate_labels(grid, user_answers, grid_answers, end_game):
    labels = []
    for i in range(16):
        if i == 0:
            labels.append("**NAODOKU**")
        elif len(grid_ids_to_letters[i]) == 1:
            labels.append(f"**{grid[f"Criteria {grid_ids_to_letters[i]}"]}**")
        elif grid_ids_to_letters[i] in user_answers :
            labels.append(user_answers[grid_ids_to_letters[i]])
        elif end_game : 
            labels.append(f"Voir les {len(grid_answers[grid_ids_to_letters[i]])} solutions")
        else :
            labels.append(f"{len(grid_answers[grid_ids_to_letters[i]])} arrêts possibles")
    return labels




# ------------------ Hints functions ---------------
# Hint 1
def convert_word_to_dashes(word):
    spaces = [i for i in range(len(word)) if word[i] == " "]
    dashes = [i for i in range(len(word)) if word[i] == "-"]
    new = ["_"]*len(word)
    for idx in spaces:
        new[idx]=" "
        new[idx+1]=word[idx+1]
    for idx in dashes:
        new[idx]="-"
        new[idx+1]=word[idx+1]
    new[0]=word[0]
    res = "".join(new)
    return res

# Hint 2
def get_lines_from_station(station):
    lines_filter = "Sur la ligne"
    lines_crit_cols = ["Nom arret"] + [col for col in truth_table.columns if lines_filter in col]
    filtered_truth_table = truth_table[lines_crit_cols]
    station_row = filtered_truth_table[filtered_truth_table["Nom arret"] == station]
    true_lines =[col[-1] for col in station_row.columns if station_row[col].reset_index(drop=True)[0] == "VRAI"]
    return true_lines

# Hint 3
def multiple_choice_question(cell, solutions, user_answers, all_stations_names):
    cell_solutions = solutions[cell]
    crit1, crit2 = st.session_state.grid[f"Criteria {list(cell)[0]}"], st.session_state.grid[f"Criteria {list(cell)[1]}"]
    remaining_stops = [stop for stop in all_stations_names if ((stop not in cell_solutions) & (stop not in user_answers) & (stop != " "))]
    stop_crit1 = [stop for stop in remaining_stops if truth_table[truth_table["Nom arret"] == stop][crit1].reset_index(drop=True)[0]  == "VRAI"]
    stop_crit2 = [stop for stop in remaining_stops if truth_table[truth_table["Nom arret"] == stop][crit2].reset_index(drop=True)[0]  == "VRAI"]
    other_stops = stop_crit1 + stop_crit2
    false_idx = np.random.choice(len(other_stops), 3, replace=False)
    false_stops = [other_stops[int(idx)] for idx in false_idx]
    true_idx = np.random.randint(len(cell_solutions))
    true_stop = [cell_solutions[int(true_idx)]]
    res_list = false_stops+true_stop
    random.shuffle(res_list)
    return res_list

# ------------ deprecated --------------
def save_game_stats(grid, user_answers, duration):
    stats = {}
    for letter_id in col_letters + row_letters:
       stats[f"Critere {letter_id}"] = grid[f"Criteria {letter_id}"]
    for col_id in col_letters:
       for row_id in row_letters:
          stats[f"Arret {col_id+row_id}"] = user_answers[col_id+row_id]
    
    stats["Temps"] = str(duration)
    
    stats_cols = [f"Critere {i}" for i in col_letters+row_letters] + [f"Arret {col_id+row_id}" for col_id in col_letters for row_id in row_letters] + ["Temps"]
    
    stats_df = pd.DataFrame([stats], columns=stats_cols, dtype=str)
    
    stats_df.to_csv(stats_save_file, sep=";", mode="a", encoding="utf-8", header=False, index=False)
