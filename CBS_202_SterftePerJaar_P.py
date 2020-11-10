# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     09-11-2020: Eerste versie
#
# =========================================================================

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# get current directory
root = Path.cwd()

# Output van pandas configureren
pd.set_option('display.max_columns', None)  # Toon alle kolommen
pd.set_option('display.max_rows', None)  # Toon alle rijen
pd.set_option('display.width', None)  # Zet alle kolommen naast elkaar

# Lees het opgslagen dataframe in
dataPath = Path(str(root) + '/data/df_37556.dataframe')
df_bevolking = pd.read_pickle(dataPath)

# Voeg een kolom toe waarin het aantal overledenen als percentage staat ipv 'per 1000'
df_bevolking['Fractie'] = df_bevolking['OverledenenRelatief_77']/10

# Maak van de jaren integers
df_bevolking['Perioden'] = df_bevolking['Perioden'].astype(int)

# Maak een subset met alleen de data voor de garfiek
df_grafiekdata = df_bevolking[['Perioden', 'Fractie']]

# Hernoem de kolommen
df_grafiekdata.columns = ['Jaar', 'Fractie']

# ---- Overledenen voor 2019 handmatig toevoegen. Afkomstig uit dataset 70895ned ---
overledenen = 151793
inwoners = 17282000
fractie = round(overledenen / inwoners * 100, 3)
df_grafiekdata.at[120, 'Fractie'] = fractie  # 120 is de index voor het jaar 2019

# ----------  Grafiek ----------
fig, ax = plt.subplots()
ax.plot(df_grafiekdata['Jaar'], df_grafiekdata['Fractie'])

fig.suptitle('Overledenen per jaar als percentage van het aantal inwoners op 1 januari', fontsize=15, ha='center')
ax.set_xlabel('Jaar', fontsize=10)
ax.set_ylabel('% overleden', fontsize=10)

ax.set_xlim(1900, 2020)
ax.set_ylim(0, 2)

# --------------------------------------- annotaties ---------------------------------
ax.annotate(
    '1918 - 1e Wereldoorlog - Spaanse griep pandemie', fontsize=8
    , xy=(1918, 1.74), xytext=(1922, 1.85)
    , arrowprops=dict(facecolor='red', edgecolor='red', width=2, headwidth=6, headlength=6, shrink=0.07)
)
ax.annotate(
    '1945 - 2e Wereldoorlog - Hongerwinter', fontsize=8
    , xy=(1945, 1.53), xytext=(1949, 1.64)
    , arrowprops=dict(facecolor='red', edgecolor='red', width=2, headwidth=6, headlength=6, shrink=0.07)
)
ax.annotate(
    '1993 - Griepgolf', fontsize=8
    , xy=(1993, 0.91), xytext=(1997, 1.02)
    , arrowprops=dict(facecolor='green', edgecolor='green', width=1, headwidth=4, headlength=4, shrink=0.07)
)

ax.annotate(
    '2018 - Griepgolf', fontsize=8
    , xy=(2018, 0.89), xytext=(2009, 1)
    , arrowprops=dict(facecolor='green', edgecolor='green', width=1, headwidth=4, headlength=4, shrink=0.07)
)

# Text buiten het plotgebied (0,0 is bottom left, 1.1 is top right)
plt.gcf().text(0.85, 0.05, 'Bron: CBS, dataset 37556', fontsize=6)

# Maximaliseren op het scherm
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')
plt.grid('True')
plt.show()
