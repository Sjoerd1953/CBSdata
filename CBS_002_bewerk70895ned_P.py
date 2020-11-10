# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     03-11-2020: Eerste versie
#   1.1     09-11-2020: Ophalen en wegschrijven data naar subdirectory
#
# =========================================================================

import pandas as pd
from pathlib import Path

# get current directory
root = Path.cwd()
dataPath = Path(str(root) + '/data/df_70895ned.dataframe')

# Output van pandas configureren
pd.set_option('display.max_columns', None)  # Toon alle kolommen
pd.set_option('display.max_rows', None)  # Toon alle rijen
pd.set_option('display.width', None)  # Zet alle kolommen naast elkaar

# Dataframe ophalen van disk
df_70895ned = pd.read_pickle(dataPath)

# Corrigeren typo's
df_70895ned['Perioden'] = df_70895ned['Perioden'].replace(['1995 '], '1995')
df_70895ned['Perioden'] = df_70895ned['Perioden'].replace(['2020 week10'], '2020 week 10')

# Verwijder 1995 week 0 - hoort niet bij 1995
indexNames = df_70895ned[df_70895ned['Perioden'].str.contains('1995 week 0')].index
df_70895ned = (df_70895ned.drop(indexNames))

# Splits het dataframe in weekdata en jaardata
df_70895ned_jaar = df_70895ned[df_70895ned['Perioden'].apply(len) == 4]
df_70895ned_week = df_70895ned[df_70895ned['Perioden'].apply(len) != 4]

# re-indexeer de dataframes
df_70895ned_jaar = df_70895ned_jaar.reset_index(drop=True)
df_70895ned_week = df_70895ned_week.reset_index(drop=True)

# ----------------------------------------------------------------------------------------------
# In de dataset staan onvolledige weken. CBS houdt de weeknummering aan waardoor de meeste weken
# 1, 52 en 53 minder dan 7 dagen bevatten. Daarnaast komt er regelmatig een week 0 voor.
# Deze weken worden samengevoegd tot weken van 7 dagen. De weken 0 verdwijnen en elk jaar begint
# met een volledige week 1 en eindigt met een volledige week 52. Eens in de zoveel jaar is er
# een volledige week 53.
# ----------------------------------------------------------------------------------------------

# Voeg het aantal overledenen in een week 0 samen met de voorgaande week 52 of 53
# en maak het de nieuwe week 52 of 53. Verwijder week 0.

# Maak een lijst van de rijen die week 0 bevatten
li_week_0 = df_70895ned_week.index[df_70895ned_week['Perioden'].str.contains('week 0')].tolist()

# Doorloop de lijst en maak de aanpassingen
for row in li_week_0:
    # Haal het aantal overledenen uit week 0 en week 52/53 op tel bij elkaar op
    this_row = df_70895ned_week.at[row, 'Overledenen_1']
    prev_row = df_70895ned_week.at[row - 1, 'Overledenen_1']
    new_row = this_row + prev_row

    # Haal het weeknummer op en verwijder de toevoeging (x dagen)
    week = df_70895ned_week.at[row - 1, 'Perioden']
    new_week = week[0:12]

    # Maak de nieuwe week 52/53 aan
    df_70895ned_week.at[row - 1, 'Overledenen_1'] = new_row
    df_70895ned_week.at[row - 1, 'Perioden'] = new_week

    # Verijder week 0
    df_70895ned_week = df_70895ned_week.drop([row])

# Voeg het aantal overledenen in een onvolledige week 1 samen met de voorgaande week 53
# en maak het de nieuwe volledige week 1. Verwijder week 53.

# Maak een lijst van de rijen die onvolledige week 1 bevatten
li_week_1 = df_70895ned_week.index[df_70895ned_week['Perioden'].str.contains('week 1 ')].tolist()

# Doorloop de lijst en maak de aanpassingen
for row in li_week_1:
    # Haal het aantal overledenen uit week 1 en week 53 op tel bij elkaar op
    this_row = df_70895ned_week.at[row, 'Overledenen_1']
    prev_row = df_70895ned_week.at[row - 1, 'Overledenen_1']
    new_row = this_row + prev_row

    # Haal het weeknummer op en verwijder de toevoeging (x dagen)
    week = df_70895ned_week.at[row, 'Perioden']
    new_week = week[0:11]

    # Maak de nieuwe week 1 aan
    df_70895ned_week.at[row, 'Overledenen_1'] = new_row
    df_70895ned_week.at[row, 'Perioden'] = new_week

    # Verijder week 53
    df_70895ned_week = df_70895ned_week.drop([row - 1])

# re-indexeer het dataframe
df_70895ned_week = df_70895ned_week.reset_index(drop=True)

# sla de dataframes op
dataPath = Path(str(root) + '/data/df_70895ned_week.dataframe')
df_70895ned_week.to_pickle(dataPath)
dataPath = Path(str(root) + '/data/df_70895ned_jaar.dataframe')
df_70895ned_jaar.to_pickle(dataPath)

# Pas het week-dataframe aan voor grafische weergave

# Voeg kolommen Jaar en Week toe door kolom Perioden te splitsen met ' week ' als separator
df_70895ned_week[['Jaar', 'Week']] = df_70895ned_week.Perioden.str.split(' week ', expand=True)

# Verwijder kolom Perioden
del df_70895ned_week['Perioden']

# Herschik de kolommen
df_70895ned_week = df_70895ned_week[['ID', 'Jaar', 'Week', 'Overledenen_1', 'Geslacht', 'LeeftijdOp31December']]

# Hernoem de kolommen
df_70895ned_week.columns = ['ID', 'Jaar', 'Week', 'Overledenen', 'Geslacht', 'Leeftijd']

# Maak van de kolommen Jaar en Week integers
df_70895ned_week['Jaar'] = df_70895ned_week['Jaar'].astype(int)
df_70895ned_week['Week'] = df_70895ned_week['Week'].astype(int)

# Sla het dataframe op
dataPath = Path(str(root) + '/data/df_weekdata.dataframe')
df_70895ned_week.to_pickle(dataPath)
