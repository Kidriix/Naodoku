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