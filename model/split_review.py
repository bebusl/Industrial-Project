import pandas as pd

reviews = pd.read_csv('./output/reviews.txt', header=None)

reviews = reviews.sample(frac=1).reset_index(drop=True)

split_size = 3
review_count = 1000

for i in range(split_size):
    prev_i, next_i = i * review_count, (i + 1) * review_count
    split_df = reviews.iloc[prev_i: next_i, :]

    split_df.to_csv(f"./output/reviews_{i}.txt", index=False, header=False)
