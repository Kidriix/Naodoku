import numpy as np
import pandas as pd
from itertools import combinations, permutations



pairs = pd.read_csv("20260728_Projet_NAO_paires.csv", sep=";", encoding="latin-1")
criteria_names = np.unique(pairs["Paire 1"].tolist())

all_criteria_comb = [comb for comb in combinations(criteria_names, 6)]
output_cols = ["Criteria A", "Criteria B", "Criteria C", "Criteria D", "Criteria E", "Criteria F", "Stations AD", "Stations AE", "Stations AF", "Stations BD", "Stations BE", "Stations BF", "Stations CD", "Stations CE", "Stations CF"]
result = pd.DataFrame(columns=output_cols)

def is_valid_grid(grid):
    res = True

    colA, colB, colC, rowD, rowE, rowF = grid
    nb_res = []
    for col in [colA, colB, colC]:
        for row in [rowD, rowE, rowF]:
            nb = pairs[((pairs["Paire 1"]==str(col))) & (pairs["Paire 2"]==str(row)) | ((pairs["Paire 2"]==str(col)) & (pairs["Paire 1"]==str(row)))]["Nb arrets"].tolist()[0]
            if nb == 0:
                res = False
                return res, nb_res
            nb_res.append(nb)
    return res, nb_res

#nb_comb = len(all_criteria_comb)
for (i, combination) in enumerate(all_criteria_comb):
    if i % 100 ==0 :
        print(i)

    (A, B, C, D, E, F) = combination
    all_comb_pairs = [comb for comb in combinations(combination, 2)]
    nb_stations_pairs = [pairs[((pairs["Paire 1"]==str(crit1)) & (pairs["Paire 2"]==str(crit2))) | ((pairs["Paire 2"]==str(crit1)) & (pairs["Paire 1"]==str(crit2)))]["Nb arrets"].tolist()[0] for (crit1, crit2) in all_comb_pairs]

    nb_zeros = nb_stations_pairs.count(0)
    nb_non_zeros = len(nb_stations_pairs)-nb_zeros

    if nb_non_zeros >= 9 :
    
        comb_wo_A = (B, C, D, E, F)
        all_pairs_without_A = [comb for comb in combinations(comb_wo_A, 2)]
        all_triplets_with_A = [ (A, p1, p2) for (p1, p2) in all_pairs_without_A]
        all_other_triplets = [tuple(list(filter(lambda x: (x != p1) & (x != p2), comb_wo_A))) for (p1, p2) in all_pairs_without_A]
        for (triplet_A, triplet_other) in zip(all_triplets_with_A, all_other_triplets):
            grid = triplet_A + triplet_other
            valid_grid, nb_grid = is_valid_grid(grid)
            if valid_grid :
                row_result = {
                    "Criteria A": str(triplet_A[0]), 
                    "Criteria B": str(triplet_A[1]),
                    "Criteria C": str(triplet_A[2]), 
                    "Criteria D": str(triplet_other[0]), 
                    "Criteria E": str(triplet_other[1]), 
                    "Criteria F": str(triplet_other[2]),  
                    "Stations AD": nb_grid[0], 
                    "Stations AE": nb_grid[1], 
                    "Stations AF": nb_grid[2], 
                    "Stations BD": nb_grid[3], 
                    "Stations BE": nb_grid[4], 
                    "Stations BF": nb_grid[5], 
                    "Stations CD": nb_grid[6], 
                    "Stations CE": nb_grid[7], 
                    "Stations CF": nb_grid[8], 
                }
                result.loc[len(result)] = row_result
    if len(result) > 10000:
        break

print(len(result))
pass
result.to_csv("20260728_Projet_NAO_results.csv", sep=";", encoding='utf-8')

