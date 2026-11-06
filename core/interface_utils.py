import streamlit as st
import base64
import numpy as np
import os
from constants.svg_images import *
from constants.css_setup import *
from constants.dict_lists_setup import *
from constants.ref_path_files import *

def show_logo(lines_id):
   path_logo = [os.path.join(WK_FOLDER, ".images", f"indices de ligne_svg_picto_ligne_{line_id}.svg" for line_id in lines_id]
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

def set_font_size(labels):
    max_len = max(len(l) for l in labels)
    if max_len <= 15:
        font_size = "clamp(0.6rem, 3vw, 0.95rem)"
    elif max_len <= 30:
        font_size = "clamp(0.5rem, 2.3vw, 0.78rem)"
    elif max_len <= 45:
        font_size = "clamp(0.42rem, 1.9vw, 0.65rem)"
    else:
        font_size = "clamp(0.36rem, 1.6vw, 0.55rem)"
    return font_size

def set_cells_colors(user_answers):
    res_css = """"""
    for i in clickable_ids:
        col_row = grid_ids_to_letters[i]
        if col_row in user_answers:
            res_css += f"""
        .st-key-cell_{i} button, .st-key-cell_{i} button:disabled {{
            background-color: {color_filled} !important;
            color: {color_filled_text} !important;
            border: 1px solid {color_filled_border} !important;
        }}"""
        else:
            res_css += f"""
        .st-key-cell_{i} button, .st-key-cell_{i} button:disabled {{
            background-color: {color_empty} !important;
            color: {color_empty_text} !important;
            border: 1px solid {color_empty_border} !important;
        }}"""
    return res_css
