import pandas as pd
import os

WK_FOLDER = os.path.dirname(os.path.abspath("NAOLIB"))
DATA_FOLDER = WK_FOLDER + "/data/"
CONSTANTS_FOLDER = WK_FOLDER + "/constants/"

grids = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')
truth_table = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_table_verite.csv", sep=";", encoding='latin-1')
legend = pd.read_csv(DATA_FOLDER + "20260728_Projet_NAO_legende.csv", sep=";", encoding='latin-1')
stats_save_file = os.path.join(WK_FOLDER, ".stats", "Projet_NAO_stats.csv")

lines_logos = [
    os.path.join(WK_FOLDER, ".images", f"indices de ligne_svg_picto_ligne_{i}.svg")
    for i in range(1, 6)
]

stations_names = [" "] + sorted(truth_table["Nom arret"].tolist())
