import glob
import pandas as pd

path = "./dataset/data_*.csv"
file_list = glob.glob(path)

df = pd.DataFrame()
for file in file_list:
    temp = pd.read_csv(file)
    df = pd.concat([df, temp])

df.drop_duplicates(inplace=True)

df.to_csv("./output/merge_data.csv", index=False)
