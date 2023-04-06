import csv, random

stats = ["PPG", "RPG", "APG", "FG%"]

class load_data:
    careers = {}

    def __init__(self):
        with open("ucla_database.csv") as u:
            reader = csv.DictReader(u, delimiter=',')
            for row in reader:
                load_data.careers[row["Player"]] = {"PPG":safe_float(row["PPG"]), "RPG":safe_float(row["RPG"]), "APG":safe_float(row["APG"]), "FG%":safe_float(row["FG%"]), "3P%":safe_float(row["3P%"]), "FT%":safe_float(row["FT%"])}

    @staticmethod
    def random_career():
        return  random.choice(list(load_data.careers.keys()))

    @staticmethod
    def get_stat(stat, name):
        return load_data.careers[name][stat]

def safe_float(str):
        if (str==''):
            return 0
        return float(str)

def compareStat(stat, career1, career2):
     career1Stat = load_data.get_stat(stat, career1)
     career2Stat = load_data.get_stat(stat, career2)
     if (career1Stat == career2Stat):
          return {"value" : career1Stat, "equality" : 1}
     elif (career1Stat > career2Stat):
          return {"value" : career1Stat, "equality" : 2}
     else:
        return {"value" : career1Stat, "equality" : 0}

def compareStats(dict, career1, career2):
    for stat in stats:
        dict[stat] = compareStat(stat, career1, career2)
     
def compareCareers(career1, career2):
    playerComparison = {}
    playerComparison["player"] = career1

    if (career1 == career2):
        playerComparison["answer"] = True
    else:
        playerComparison["answer"] = False

    compareStats(playerComparison, career1, career2)

    return playerComparison