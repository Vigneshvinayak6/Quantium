import pandas as pd
import glob
import os
csv_files = glob.glob(os.path.join("C:/Users/Velan/PycharmProjects/quantium", "*.csv"))
df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)
df.to_csv("combined_file.csv", index=False)