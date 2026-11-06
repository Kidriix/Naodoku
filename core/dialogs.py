import streamlit as st
from constants.texts import *
from constants.ref_files_paths import *
from constants.dict_lists_setup import *

@st.dialog("Comment ça marche ?")
def welcome(explain_hints=False):
    tabs_names = ["Règles"]
    if explain_hints:
       tabs_names.append("Indices")
    rules_tabs = st.tabs(tabs_names)
    rules_tabs[0].markdown(intro_text_1)
    rules_tabs[0].image(lines_logos)
    rules_tabs[0].markdown(intro_text_2)

    if explain_hints:
       rules_tabs[1].markdown(intro_hints_text)
       with rules_tabs[1].expander("**Première Lettre**"):
            st.markdown(hint_1_text)
       with rules_tabs[1].expander("**Ligne**"):
            st.markdown(hint_2_text)
       with rules_tabs[1].expander("**QCM** (**Q**uestion à **C**hoix **M**ultiples)"):
            st.markdown(hint_3_text)
    st.session_state.first_opening = False

@st.dialog("Description")
def describe_criteria(cell_id):
   crit = st.session_state.grid[f"Criteria {grid_ids_to_letters[cell_id]}"]
   desc = legend[legend["Nom critere"]==st.session_state.grid[f"Criteria {grid_ids_to_letters[cell_id]}"]]["Description"].tolist()[0]
   st.title(f"**{crit}**")
   st.markdown(desc)

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