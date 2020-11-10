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

import cbsodata
import pandas as pd
from pathlib import Path

# identifier of the dataset as found in 'Tabel informatie' on CBS StatLine
# ------------------------------------------------------------------------------
# 70895ned  : Overledenen; geslacht en leeftijd, per week.
# 37296ned  : Bevolking; kerncijfers
# 37556     : Bevolking, huishoudens en bevolkingsontwikkeling; vanaf 1899
# 7233      : Overledenen; doodsoorzaak (uitgebreide lijst), leeftijd, geslacht
# ------------------------------------------------------------------------------

identifier = '37556'

# get current directory
root = Path.cwd()

# Download the datasets as Pandas dataframe from CBS Statline and store datasets a binary files

# ----- Metadata -----
df_dataset = pd.DataFrame(cbsodata.get_meta(identifier, 'DataProperties'))
# create data path fo storage
dataPath = Path(str(root) + '/data/df_meta_' + identifier + '.dataframe')
# save dataframe
df_dataset.to_pickle(dataPath)
print('Metadata gedownload en opgeslagen')

# ----- Dataset -----
df_dataset = pd.DataFrame(cbsodata.get_data(identifier))
# create data path fo storage
dataPath = Path(str(root) + '/data/df_' + identifier + '.dataframe')
# save dataframe
df_dataset.to_pickle(dataPath)
print('Dataset gedownload en opgeslagen')