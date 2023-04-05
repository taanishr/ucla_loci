import csv, random

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
    def get_stat(name, stat):
        return load_data.careers[name][stat]

def compareCareerStat(career1, career2, stat):
    if (load_data.get_stat(career1, stat) > load_data.get_stat(career2, stat)):
        return True
    else:
        return False

def safe_float(str):
        if (str==''):
            return 0
        return float(str)
