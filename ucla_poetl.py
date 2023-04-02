import csv
import random

solved = False

careers = {}

def safe_float(str):
    if (str==''):
        return 0
    return float(str)

with open("ucla_database.csv") as u:
    reader = csv.DictReader(u, delimiter=',')
    for row in reader:
        careers[row["Player"]] = {"PPG":safe_float(row["PPG"]), "RPG":safe_float(row["RPG"]), "APG":safe_float(row["APG"]), "FG%":safe_float(row["FG%"]), "3P%":safe_float(row["3P%"]), "FT%":safe_float(row["FT%"])}

random_career = random.choice(list(careers.keys()))

print([random_career])
print(careers[random_career])
                              
for i in range(5, 0, -1):
    print(f"YOU HAVE {i} GUESSES ") if i > 1 else print(f"YOU HAVE {i} GUESS")
    guess = input("Enter your guess:\n")
    while (guess not in careers.keys()):
        guess = input("Please enter a player that attended UCLA\n")
    if (guess == random_career):
        solved = True
        break
    else:
        ppg = "ppg: ↑" if (careers[guess]["PPG"] < careers[random_career]["PPG"]) else "ppg: ↓"
        rpg = "rpg: ↑" if (careers[guess]["RPG"] < careers[random_career]["RPG"]) else "rpg: ↓"
        apg = "apg: ↑" if (careers[guess]["APG"] < careers[random_career]["APG"]) else "apg: ↓"
        fg = "fg%: ↑" if (careers[guess]["FG%"] < careers[random_career]["FG%"]) else "fg%: ↓"
        print(f"{ppg} | {rpg} | {apg} | {fg}\n")

if (solved):
    print("Solved!")
else:
    print(f"The player was {random_career} \n")



    
