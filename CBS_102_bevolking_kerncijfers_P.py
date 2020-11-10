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

df_kerncijfers['0 tot 65 jaar'] = df_kerncijfers['TotaleBevolking_1'] - (df_kerncijfers['k_65Tot80Jaar_13'] + df_kerncijfers['k_80JaarOfOuder_14'])
df_kerncijfers['Perioden'] = df_kerncijfers['Perioden'].astype(int)

df_grafiekdata = df_kerncijfers[['Perioden', 'TotaleBevolking_1', '0 tot 65 jaar', 'k_65Tot80Jaar_13', 'k_80JaarOfOuder_14']]
df_grafiekdata.columns = ['Jaar', 'Totaal aantal', '0 tot 65 jaar', '65 tot 80 jaar', '80 jaar of ouder']

# De in de grafiek gewenste jaren
jaren = range(2010, 2021, 1)

print(df_grafiekdata[df_grafiekdata['Jaar'].isin(jaren)])
