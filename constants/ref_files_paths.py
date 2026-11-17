import pandas as pd
import os
import base64

WK_FOLDER = os.path.dirname(os.path.abspath("NAOLIB"))
DATA_FOLDER = WK_FOLDER + "/data/"
CONSTANTS_FOLDER = WK_FOLDER + "/constants/"
IMAGES_FOLDER = WK_FOLDER + "/.images/"

grids = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')
stats_save_file = os.path.join(WK_FOLDER, ".stats", "Projet_NAO_stats.csv")

lines_logos = [
    os.path.join(IMAGES_FOLDER, "lines_icons", f"indices de ligne_svg_picto_ligne_{i}.svg")
    for i in range(1, 6)
]

transport_logos = [
    os.path.join(IMAGES_FOLDER, "transport_icons", f"pictos_svg_nao_{mode}.svg")
    for mode in ["bus", "car", "cycliste", "marche", "train", "navibus", "tram", "voiture"]
]

def svg_to_data_uri(svg_path):
    with open(svg_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"

icon_uri = [svg_to_data_uri(f"static/indices_de_ligne_svg_picto_ligne_{i}_small.svg") for i in range(1,6)]
lines_emojis_list = [f"![line_{i}]({icon_uri[i-1]})" for i in range(1, 6)]

stations_names = [" "] + sorted(truth_table["Nom arret"].tolist())
