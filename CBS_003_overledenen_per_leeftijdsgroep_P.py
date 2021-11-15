# =========================================================================
#
#   Auteur: S. van Staveren
#   mail: sjoerd@van-staveren.net
#
#   Versiegeschiedenis:
#   1.0     02-11-2020: Eerste versie
#   1.1     09-11-2020: Ophalen data uit subdirectory
#   1.2     13-11-2020: Scherm maximaliseren aangepast
#   1.3     15-11-2021: Huidig jaar en afgelopen 4 jaren automatisch bepaald
#                       Aanpassing aan Pandas 1.3.4 (jaren als integers)
#
# =========================================================================

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from pathlib import Path

# get current directory
root = Path.cwd()

# Output van pandas configureren
pd.set_option('display.max_columns', None)  # Toon alle kolommen
pd.set_option('display.max_rows', None)  # Toon alle rijen
pd.set_option('display.width', None)  # Zet alle kolommen naast elkaar

# Lees het opgslagen dataframe in
dataPath = Path(str(root) + '/data/df_weekdata.dataframe')
df_weekdata = pd.read_pickle(dataPath)

# Bepaal het rapportage weeknummer voor huidige jaar
nu = datetime.datetime.now()
datum = nu.date()
jaar = datum.strftime('%Y')
jaar = int(jaar)

df_ditjaar = df_weekdata[
    (df_weekdata['Geslacht'] == 'Totaal mannen en vrouwen') &
    (df_weekdata['Leeftijd'] == 'Totaal leeftijd') &
    (df_weekdata['Jaar'] == jaar)
    ]
maxweek = (max(df_ditjaar['Week']))

# Filteren op Totaal mannen en vrouwen
df_TotaalMV = df_weekdata[(df_weekdata['Geslacht'] == 'Totaal mannen en vrouwen')]

# Groeperen op Leeftijd (4 groepen)
df_grouped_TotaalMV_Leeftijd = df_TotaalMV.groupby('Leeftijd')

# Datasets voor de grafieken aanmaken
df_graph_65min = df_grouped_TotaalMV_Leeftijd.get_group('0 tot 65 jaar')[['Jaar', 'Week', 'Overledenen']]
df_graph_65tot80 = df_grouped_TotaalMV_Leeftijd.get_group('65 tot 80 jaar')[['Jaar', 'Week', 'Overledenen']]
df_graph_80plus = df_grouped_TotaalMV_Leeftijd.get_group('80 jaar of ouder')[['Jaar', 'Week', 'Overledenen']]
df_graph_totaal = df_grouped_TotaalMV_Leeftijd.get_group('Totaal leeftijd')[['Jaar', 'Week', 'Overledenen']]

# De in de grafiek gewenste jaren - huidig jaar en 4 voorgaande jaren
jaren = [jaar]
for i in range(1, 5):
    jaar = jaar - 1
    jaren.append(jaar)

# Pivot tabelen maken met de voor grafiek noodzakelijke gegevens
pivot_totaal = df_graph_totaal[(df_graph_totaal['Jaar'].isin(jaren))].pivot('Week', 'Jaar', 'Overledenen')
pivot_65min = df_graph_65min[(df_graph_65min['Jaar'].isin(jaren))].pivot('Week', 'Jaar', 'Overledenen')
pivot_65tot80 = df_graph_65tot80[(df_graph_65tot80['Jaar'].isin(jaren))].pivot('Week', 'Jaar', 'Overledenen')
pivot_80plus = df_graph_80plus[(df_graph_80plus['Jaar'].isin(jaren))].pivot('Week', 'Jaar', 'Overledenen')

# Toon de gegevens
print('-------------------- Alle leeftijden --------------------')
print(pivot_totaal)
print('--------------------- 0 tot 65 jaar ---------------------')
print(pivot_65min)
print('--------------------- 65 tot 80 jaar --------------------')
print(pivot_65tot80)
print('--------------------- 80 jaar en ouder ------------------')
print(pivot_80plus)

# ----------  Grafiek ----------
fig, axs = plt.subplots(2, 2)

# Assen en lijnen configureren
colors = ['#ff00bf', '#00ff00', '#0000ff', '#ff0000', '#000000']
linestyles = ['--', '--', '--', '--', '-']
xlim = (1, 53)
ylim = (0, 5500)
ylabel = 'Aantal'

# Grafieken maken
pivot_totaal.plot(ax=axs[0, 0], kind='line', color=colors, style=linestyles, xlim=xlim, ylim=ylim, ylabel=ylabel)
pivot_65min.plot(ax=axs[0, 1], kind='line', color=colors, style=linestyles, xlim=xlim, ylim=ylim, ylabel=ylabel)
pivot_65tot80.plot(ax=axs[1, 0], kind='line', color=colors, style=linestyles, xlim=xlim, ylim=ylim, ylabel=ylabel)
pivot_80plus.plot(ax=axs[1, 1], kind='line', color=colors, style=linestyles, xlim=xlim, ylim=ylim, ylabel=ylabel)

# Titels en leganda toevoegen
axs[0, 0].set_title('Alle leeftijden')
axs[0, 0].legend(loc='best', fontsize=8)
axs[0, 1].set_title('0 tot 65 jaar')
axs[0, 1].legend(loc='best', fontsize=8)
axs[1, 0].set_title('65 tot 80 jaar')
axs[1, 0].legend(loc='best', fontsize=8)
axs[1, 1].set_title('80 jaar en ouder')
axs[1, 1].legend(loc='best', fontsize=8)

# Titel voor de 4 subgrafieken toevoegen
fig.suptitle('Totaal aantal sterfgevallen per week. Totaal en naar leeftijdsgroep. 2021 t/m week ' + str(maxweek), fontsize=15)

# Text buiten het plotgebied (0,0 is bottom left, 1.1 is top right)
plt.gcf().text(0.85, 0.05, 'Bron: CBS, dataset 70895ned', fontsize=6)

# Maximaliseren op het scherm - werkt niet op elke PC, vandaar 'try'
try:
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()
except:
    plt.show()
