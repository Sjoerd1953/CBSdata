# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     09-11-2020: Eerste versie
#   1.1     13-11-2020: Scherm maximaliseren aangepast
#   1.2     21-11-2020: Trendlijn 2010 - 2019 met betrouwbaarheids interval
#                       maken mbv scipy.stats
#
# =========================================================================

import pandas as pd
import matplotlib.pyplot as plt
import math as m
from scipy import stats
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


# data van 2010 t/m 2019 in lists zetten
x = df_fractie['Jaar'][0:10].tolist()
y1 = df_fractie['Totaal leeftijd'][0:10].tolist()
y2 = df_fractie['0 tot 65 jaar'][0:10].tolist()
y3 = df_fractie['65 tot 80 jaar'][0:10].tolist()
y4 = df_fractie['80 jaar of ouder'][0:10].tolist()

# regressiegegevens van 2010 tot 2019 berekenen
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(x, y1)
slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(x, y2)
slope3, intercept3, r_value3, p_value3, std_err3 = stats.linregress(x, y3)
slope4, intercept4, r_value4, p_value4, std_err4 = stats.linregress(x, y4)

# regressielijn 2010 tot 2020 berekenen en in lists zetten
jaren = []
trend1 = []
trend2 = []
trend3 = []
trend4 = []

fill1max = []
fill1min = []

fill2max = []
fill2min = []

fill3max = []
fill3min = []

fill4max = []
fill4min = []

# factor voor de berekening van het 99% betrouwbaarheidsinterval in de grafiek
# standaarddeviatie is std_err * sqrt(n) (n = 10: 2010 t/m 2019)
bi = 2.576

for jaar in range(2010, 2021):
    jaren.append(jaar)

    trend1.append(intercept1 + slope1 * jaar)
    fill1max.append(intercept1 + slope1 * jaar + bi * m.sqrt(10) * std_err1)
    fill1min.append(intercept1 + slope1 * jaar - bi * m.sqrt(10) * std_err1)

    trend2.append(intercept2 + slope2 * jaar)
    fill2max.append(intercept2 + slope2 * jaar + bi * m.sqrt(10) * std_err2)
    fill2min.append(intercept2 + slope2 * jaar - bi * m.sqrt(10) * std_err2)

    trend3.append(intercept3 + slope3 * jaar)
    fill3max.append(intercept3 + slope3 * jaar + bi * m.sqrt(10) * std_err3)
    fill3min.append(intercept3 + slope3 * jaar - bi * m.sqrt(10) * std_err3)

    trend4.append(intercept4 + slope4 * jaar)
    fill4max.append(intercept4 + slope4 * jaar + bi * m.sqrt(10) * std_err4)
    fill4min.append(intercept4 + slope4 * jaar - bi * m.sqrt(10) * std_err4)

# grafiek maken
fig, axs = plt.subplots(2, 2)

# op elke as de actuele waardes en de regressielijn tekenen
axs[0, 0].plot(df_fractie['Jaar'], df_fractie['Totaal leeftijd'], label='Per jaar')
axs[0, 0].plot(jaren, trend1, '--r', label='Trend 2010 - 2019')
axs[0, 0].fill_between(jaren, fill1max, fill1min, color='r', alpha=0.1)

axs[0, 1].plot(df_fractie['Jaar'], df_fractie['0 tot 65 jaar'], label='Per jaar')
axs[0, 1].plot(jaren, trend2, '--r', label='Trend 2010 - 2019')
axs[0, 1].fill_between(jaren, fill2max, fill2min, color='r', alpha=0.1)

axs[1, 0].plot(df_fractie['Jaar'], df_fractie['65 tot 80 jaar'], label='Per jaar')
axs[1, 0].plot(jaren, trend3, '--r', label='Trend 2010 - 2019')
axs[1, 0].fill_between(jaren, fill3max, fill3min, color='r', alpha=0.1)

axs[1, 1].plot(df_fractie['Jaar'], df_fractie['80 jaar of ouder'], label='Per jaar')
axs[1, 1].plot(jaren, trend4, '--r', label='Trend 2010 - 2019')
axs[1, 1].fill_between(jaren, fill4max, fill4min, color='r', alpha=0.1)

fig.suptitle('Relatieve sterfte per jaar en per leeftijdscategorie t/m week: ' + str(max_week) + '\n (2010 t/m 2020)',
             fontsize=25)

fig.text(0.5, 0.04, 'Jaar', ha='center', fontsize=15)
fig.text(0.04, 0.5, 'Relatieve sterfte (%)', va='center', rotation='vertical', fontsize=15)

axs[0, 0].set_title('Alle leeftijden')
axs[0, 0].set_xlim(2010, 2020)
axs[0, 0].set_ylim(0.6, 1)
axs[0, 0].grid()
axs[0, 0].legend()

axs[0, 1].set_title('0 tot 65 jaar')
axs[0, 1].set_xlim(2010, 2020)
axs[0, 1].set_ylim(0.12, 0.16)
axs[0, 1].grid()
axs[0, 1].legend()

axs[1, 0].set_title('65 tot 80 jaar')
axs[1, 0].set_xlim(2010, 2020)
axs[1, 0].set_ylim(1.4, 2)
axs[1, 0].grid()
axs[1, 0].legend()

axs[1, 1].set_title('80 jaar en ouder')
axs[1, 1].set_xlim(2010, 2020)
axs[1, 1].set_ylim(9, 10.25)
axs[1, 1].grid()
axs[1, 1].legend()

# Text buiten het plotgebied (0,0 is bottom left, 1.1 is top right)
plt.gcf().text(0.85, 0.05, 'Bron: CBS, datasets 37296ned en 70895ned', fontsize=6)

# Maximaliseren op het scherm - werkt niet op elke PC, vandaar 'try'
try:
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()
except:
    plt.show()
