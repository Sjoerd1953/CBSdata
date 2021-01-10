# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     22-11-2020: Eerste versie
#
# =========================================================================

import pandas as pd
import matplotlib.pyplot as plt
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

# of andere week
# max_week =

# Cumulatieve som per jaar, geslacht en leeftijd.
df_weekdata['Overledenen Totaal'] = df_weekdata.groupby(['Jaar', 'Geslacht', 'Leeftijd'])['Overledenen'].cumsum(axis=0)

# Selectie voor grafiek
df_selectie_weekdata = df_weekdata[
    (df_weekdata['Week'] == max_week) & (df_weekdata['Geslacht'] == 'Totaal mannen en vrouwen') & (
        df_weekdata['Jaar'].isin(jaren))]

# Maak pivot tabel van selectie
df_weekdata_pivot = df_selectie_weekdata.pivot('Jaar', 'Leeftijd', 'Overledenen Totaal')

# Maak van de pivot tabel een dataframe
df_weekdata_pivot.columns.name = None
df_weekdata_pivot = df_weekdata_pivot.reset_index()

# Wijzig de kolom volgorde
df_weekdata_pivot = df_weekdata_pivot[
    ['Jaar', 'Totaal leeftijd', '0 tot 65 jaar', '65 tot 80 jaar', '80 jaar of ouder']]

# Maak de Jaar kolom tot index
df_weekdata_pivot = df_weekdata_pivot.set_index('Jaar')

# Deel de twee dataframes op elkaar en maak procenten van de fractie
df_fractie = df_weekdata_pivot / df_grafiekdata * 100
df_fractie = df_fractie.reset_index()

df_verschil = df_fractie.copy()

# Voor elke leeftijdsgroep het verschil tov het voorgaande jaar bepalen
df_verschil['Totaal leeftijd'] = df_verschil['Totaal leeftijd'].diff()
df_verschil['0 tot 65 jaar'] = df_verschil['0 tot 65 jaar'].diff()
df_verschil['65 tot 80 jaar'] = df_verschil['65 tot 80 jaar'].diff()
df_verschil['80 jaar of ouder'] = df_verschil['80 jaar of ouder'].diff()

# Voor elke leeftijdsgroep het gemiddelde verschil en standaard deviatie berekenen
tot_gem = df_verschil['Totaal leeftijd'][0:10].mean()
tot_std = df_verschil['Totaal leeftijd'][0:10].std()

t65_gem = df_verschil['0 tot 65 jaar'][0:10].mean()
t65_std = df_verschil['0 tot 65 jaar'][0:10].std()

v65t80_gem = df_verschil['65 tot 80 jaar'][0:10].mean()
v65t80_std = df_verschil['65 tot 80 jaar'][0:10].std()

v80_gem = df_verschil['80 jaar of ouder'][0:10].mean()
v80_std = df_verschil['80 jaar of ouder'][0:10].std()

# grafiek maken
fig, axs = plt.subplots(2, 2)

# op elke as de actuele waardes en het gemiddelde +/- 1.96 x std plotten
axs[0, 0].plot(df_verschil['Jaar'][:10], df_verschil['Totaal leeftijd'][:10], color='black', label='2010 - 2019')
axs[0, 0].plot(df_verschil['Jaar'][9:], df_verschil['Totaal leeftijd'][9:], color='orange', label='2020')
axs[0, 0].hlines(y=tot_gem, xmin=df_verschil['Jaar'][0], xmax=df_verschil['Jaar'][-1:], color='r', linestyle='-', label='Gemiddelde 2010 - 2019')
axs[0, 0].fill_between(df_verschil['Jaar'], tot_gem - 1.96 * tot_std, tot_gem + 1.96 * tot_std, color='r', alpha=0.15, label='95% waarsch. interval')

axs[0, 1].plot(df_verschil['Jaar'][:10], df_verschil['0 tot 65 jaar'][:10],  color='black', label='2010 - 2019')
axs[0, 1].plot(df_verschil['Jaar'][9:], df_verschil['0 tot 65 jaar'][9:], color='orange', label='2020')
axs[0, 1].hlines(y=t65_gem, xmin=df_verschil['Jaar'][0], xmax=df_verschil['Jaar'][-1:], color='r', linestyle='-', label='Gemiddelde 2010 - 2019')
axs[0, 1].fill_between(df_verschil['Jaar'], t65_gem - 1.96 * t65_std, t65_gem + 1.96 * t65_std, color='r', alpha=0.15, label='95% waarsch. interval')

axs[1, 0].plot(df_verschil['Jaar'][:10], df_verschil['65 tot 80 jaar'][:10], color='black', label='2010 - 2019')
axs[1, 0].plot(df_verschil['Jaar'][9:], df_verschil['65 tot 80 jaar'][9:], color='orange', label='2020')
axs[1, 0].hlines(y=v65t80_gem, xmin=df_verschil['Jaar'][0], xmax=df_verschil['Jaar'][-1:], color='r', linestyle='-', label='Gemiddelde 2010 - 2019')
axs[1, 0].fill_between(df_verschil['Jaar'], v65t80_gem - 1.96 * v65t80_std, v65t80_gem + 1.96 * v65t80_std, color='r', alpha=0.15, label='95% waarsch. interval')

axs[1, 1].plot(df_verschil['Jaar'][:10], df_verschil['80 jaar of ouder'][:10], color='black', label='2010 - 2019')
axs[1, 1].plot(df_verschil['Jaar'][9:], df_verschil['80 jaar of ouder'][9:], color='orange', label='2020')
axs[1, 1].hlines(y=v80_gem, xmin=df_verschil['Jaar'][0], xmax=df_verschil['Jaar'][-1:], color='r', linestyle='-', label='Gemiddelde 2010 - 2019')
axs[1, 1].fill_between(df_verschil['Jaar'], v80_gem - 1.96 * v80_std, v80_gem + 1.96 * v80_std, color='r', alpha=0.15, label='95% waarsch. interval')

# Titels
fig.suptitle('Verandering in relatieve sterfte per jaar en per leeftijdscategorie t/m week: ' + str(max_week) + '\n (2010 t/m 2020)',
             fontsize=25)
fig.text(0.5, 0.04, 'Jaar', ha='center', fontsize=15)
fig.text(0.04, 0.5, 'Verandering in relatieve sterfte tov voorgaand jaar(%)', va='center', rotation='vertical', fontsize=15)

sf = 4.5

# Assen configureren
axs[0, 0].set_title('Alle leeftijden')
axs[0, 0].set_xlim(2010, 2020)
axs[0, 0].set_ylim(tot_gem - sf * tot_std, tot_gem + sf * tot_std)
axs[0, 0].grid()
axs[0, 0].legend(loc=2, fontsize=8)

axs[0, 1].set_title('0 tot 65 jaar')
axs[0, 1].set_xlim(2010, 2020)
axs[0, 1].set_ylim(t65_gem - sf * t65_std, t65_gem + sf * t65_std)
axs[0, 1].grid()
axs[0, 1].legend(loc=2, fontsize=8)

axs[1, 0].set_title('65 tot 80 jaar')
axs[1, 0].set_xlim(2010, 2020)
axs[1, 0].set_ylim(v65t80_gem - sf * v65t80_std, v65t80_gem + sf * v65t80_std)
axs[1, 0].grid()
axs[1, 0].legend(loc=2, fontsize=8)

axs[1, 1].set_title('80 jaar en ouder')
axs[1, 1].set_xlim(2010, 2020)
axs[1, 1].set_ylim(v80_gem - sf * v80_std, v80_gem + sf * v80_std)
axs[1, 1].grid()
axs[1, 1].legend(loc=2, fontsize=8)

# Text buiten het plotgebied (0,0 is bottom left, 1.1 is top right)
plt.gcf().text(0.85, 0.05, 'Bron: CBS, datasets 37296ned en 70895ned', fontsize=6)

# Maximaliseren op het scherm - werkt niet op elke PC, vandaar 'try'
try:
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()
except:
    plt.show()
