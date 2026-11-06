row_letters = ["D", "E", "F"]
col_letters = ["A", "B", "C"]

clickable_ids = {5, 6, 7, 9, 10, 11, 13, 14, 15} 
criteria_ids = {1, 2, 3, 4, 8, 12}
grid_ids_to_letters = {1:"A", 2:"B", 3:"C", 4:"D", 5:"AD", 6:"BD", 7:"CD", 8:"E", 9:"AE", 10:"BE", 11:"CE", 12:"F", 13:"AF", 14:"BF", 15:"CF"}

difficulty_bounds = {
  "easy": {
    "min":1,
    "max":2
  },
  "normal": {
    "min":2.5,
    "max":3.5
  },
  "hard": {
    "min":4,
    "max":5
  },
}

difficulty_FR_EN = {
   "Facile": "easy",
   "Normal": "normal",
   "Difficile": "hard"
}

default_hints_state = {
      "AD" : False,
      "AE" : False,
      "AF" : False,
      "BD" : False,
      "BE" : False,
      "BF" : False,
      "CD" : False,
      "CE" : False,
      "CF" : False,
   }


