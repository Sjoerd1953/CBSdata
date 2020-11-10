# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     09-11-2020: Eerste versie
#
# =========================================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# get current directory
root = Path.cwd()

# Output van pandas configureren
pd.set_option('display.max_columns', None)  # Toon alle kolommen
pd.set_option('display.max_rows', None)  # Toon alle rijen
pd.set_option('display.width', None)  # Zet alle kolommen naast elkaar

# Lees het opgslagen dataframe in
dataPath = Path(str(root) + '/data/df_37296ned.dataframe')
df_kerncijfers = pd.read_pickle(dataPath)

df_kerncijfers['0 tot 65 jaar'] = df_kerncijfers['TotaleBevolking_1'] - (
            df_kerncijfers['k_65Tot80Jaar_13'] + df_kerncijfers['k_80JaarOfOuder_14'])
df_kerncijfers['Perioden'] = df_kerncijfers['Perioden'].astype(int)

df_grafiekdata = df_kerncijfers[
    ['Perioden', 'TotaleBevolking_1', '0 tot 65 jaar', 'k_65Tot80Jaar_13', 'k_80JaarOfOuder_14']]
df_grafiekdata.columns = ['Jaar', 'Totaal leeftijd', '0 tot 65 jaar', '65 tot 80 jaar', '80 jaar of ouder']

# De in de grafiek gewenste jaren
jaren = range(2010, 2021, 1)

df_grafiekdata = df_grafiekdata[df_grafiekdata['Jaar'].isin(jaren)]

# Maak de Jaar kolom tot index
df_grafiekdata = df_grafiekdata.set_index('Jaar')

# Open het databestand en importeer als list of dictionaries
dataPath = Path(str(root) + '/data/df_weekdata.dataframe')
df_weekdata = pd.read_pickle(dataPath)

# Laatste rapportageweek lopende jaar
df_2020 = df_weekdata[df_weekdata['Jaar'] == 2020]
max_week = max(df_2020['Week'])

# Cumulatieve som per jaar, geslacht en leeftijd.
df_weekdata['Overledenen Totaal'] = df_weekdata.groupby(['Jaar', 'Geslacht', 'Leeftijd'])['Overledenen'].cumsum(axis=0)

# Selectie voor grafiek
df_selectie_weekdata = df_weekdata[(df_weekdata['Week'] == max_week) & (df_weekdata['Geslacht'] == 'Totaal mannen en vrouwen') & (df_weekdata['Jaar'].isin(jaren))]

# Maak pivot tabel van selectie
df_weekdata_pivot = df_selectie_weekdata.pivot('Jaar', 'Leeftijd', 'Overledenen Totaal')

# Maak van de pivot tabel een dataframe
df_weekdata_pivot.columns.name = None
df_weekdata_pivot = df_weekdata_pivot.reset_index()

# Wijzig de kolom volgorde
df_weekdata_pivot = df_weekdata_pivot[['Jaar', 'Totaal leeftijd', '0 tot 65 jaar', '65 tot 80 jaar', '80 jaar of ouder']]

# Maak de Jaar kolom tot index
df_weekdata_pivot = df_weekdata_pivot.set_index('Jaar')

# Deel de twee dataframes op elkaar en maak procenten van de fractie
df_fractie = df_weekdata_pivot/df_grafiekdata * 100
df_fractie = df_fractie.reset_index()

print(df_fractie)

fig, axs = plt.subplots(2, 2)

axs[0, 0].plot(df_fractie['Jaar'], df_fractie['Totaal leeftijd'])
axs[0, 1].plot(df_fractie['Jaar'], df_fractie['0 tot 65 jaar'])
axs[1, 0].plot(df_fractie['Jaar'], df_fractie['65 tot 80 jaar'])
axs[1, 1].plot(df_fractie['Jaar'], df_fractie['80 jaar of ouder'])

fig.suptitle('Relatieve sterfte per jaar en per leeftijdscategorie t/m week: ' + str(max_week), fontsize=25)

fig.text(0.5, 0.04, 'Jaar', ha='center', fontsize=15)
fig.text(0.04, 0.5, 'Relatieve sterfte (%)', va='center', rotation='vertical', fontsize=15)

coef1 = np.polyfit(df_fractie['Jaar'], df_fractie['Totaal leeftijd'], 1)
coef2 = np.polyfit(df_fractie['Jaar'], df_fractie['0 tot 65 jaar'], 1)
coef3 = np.polyfit(df_fractie['Jaar'], df_fractie['65 tot 80 jaar'], 1)
coef4 = np.polyfit(df_fractie['Jaar'], df_fractie['80 jaar of ouder'], 1)

poly1d_fn1 = np.poly1d(coef1)
poly1d_fn2 = np.poly1d(coef2)
poly1d_fn3 = np.poly1d(coef3)
poly1d_fn4 = np.poly1d(coef4)

axs[0, 0].plot(df_fractie['Jaar'], poly1d_fn1(df_fractie['Jaar']), '--r')
axs[0, 1].plot(df_fractie['Jaar'], poly1d_fn2(df_fractie['Jaar']), '--r')
axs[1, 0].plot(df_fractie['Jaar'], poly1d_fn3(df_fractie['Jaar']), '--r')
axs[1, 1].plot(df_fractie['Jaar'], poly1d_fn4(df_fractie['Jaar']), '--r')

axs[0, 0].set_title('Alle leeftijden')
axs[0, 0].set_xlim(2010, 2020)
axs[0, 0].set_ylim(0, 1)
axs[0, 0].grid()

axs[0, 1].set_title('0 tot 65 jaar')
axs[0, 1].set_xlim(2010, 2020)
axs[0, 1].set_ylim(0, 0.2)
axs[0, 1].grid()

axs[1, 0].set_title('65 tot 80 jaar')
axs[1, 0].set_xlim(2010, 2020)
axs[1, 0].set_ylim(1, 2)
axs[1, 0].grid()

axs[1, 1].set_title('80 jaar en ouder')
axs[1, 1].set_xlim(2010, 2020)
axs[1, 1].set_ylim(8, 10)
axs[1, 1].grid()

# Text buiten het plotgebied (0,0 is bottom left, 1.1 is top right)
plt.gcf().text(0.85, 0.05, 'Bron: CBS, datasets 37296ned en 70895ned', fontsize=6)

# Maximaliseren op het scherm
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')
plt.show()
