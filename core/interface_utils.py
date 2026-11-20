import streamlit as st
import base64
import numpy as np
import os
from streamlit_js_eval import streamlit_js_eval
from time import sleep

from constants.svg_images import *
from constants.css_setup import *
from constants.dict_lists_setup import *
from constants.ref_files_paths import *

def check_layout():
    '''With JS evaluation script, gets the width and height of the device.
    Sleep a little to get the values from JS.
    Then define a layout state depending on which is bigger.
    '''
    width = streamlit_js_eval(js_expressions='window.innerWidth')
    height = streamlit_js_eval(js_expressions='screen.height')
    sleep(1)
        
    if width is not None and height is not None:
        st.session_state.width = width
        st.session_state.height = height

def once_set_layout():
    '''Search for the device layout and rerun once set.
    '''
    if 'width' not in st.session_state:
        with st.spinner('Chargement de la grille'):
            check_layout()
            st.rerun()

def show_logo(lines_id):
   path_logo = [os.path.join(IMAGES_FOLDER, "lines_icons", f"indices de ligne_svg_picto_ligne_{line_id}.svg") for line_id in lines_id]
   st.image(path_logo)

def random_logo():
    temp_logo_list = svg_logos_list.copy()
    if "chosen_svg" in st.session_state:
        temp_logo_list.remove(st.session_state.chosen_svg)
    st.session_state.chosen_svg = str(np.random.choice(temp_logo_list, 1)[0])
    st.session_state.logo_svg_b64 = base64.b64encode(st.session_state.chosen_svg.encode("utf-8")).decode("utf-8")
    del temp_logo_list

def switch_logo():
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
