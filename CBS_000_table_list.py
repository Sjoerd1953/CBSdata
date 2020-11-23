import cbsodata
import pandas as pd

# Output van pandas configureren
pd.set_option('display.max_columns', None)  # Toon alle kolommen
pd.set_option('display.max_rows', None)  # Toon alle rijen
pd.set_option('display.width', None)  # Zet alle kolommen naast elkaar
pd.set_option('display.max_colwidth', 100)  # Toont de gehele kolombreedte

toc = pd.DataFrame(cbsodata.get_table_list())

for col in toc.columns:
    print(col)


