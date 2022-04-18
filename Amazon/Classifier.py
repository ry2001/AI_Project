import pandas as pd
from transformers import pipeline
import pickle
from datetime import datetime
import random

# import required files
file_name = pd.read_pickle("Amazon/file_name.pkl")
translated_data = pd.read_pickle(f"Amazon/{file_name}/translated.pkl")

# to check how much time needed to finish classification
print(f'start: {datetime.now()}')

# take a small portion of data to test the accuracy of the classifier
random.seed(100)
rand_lst = random.sample(range(len(translated_data)), 1000)

candidates = ["battery","screen","strap", "others"] 

classifier = pipeline("zero-shot-classification", device = 0) #if have gpu
# classifier = pipeline("zero-shot-classification")           #if no gpu

full_results_text = []

# put the results into a list
for i in rand_lst:
    full_results_text.append(classifier(translated_data[i], candidate_labels = candidates))

classified_text = []
results_text = []

# we will only use the results if the confidence level is more than 50%
# filter out many useless or not accurate results
for i in range(len(full_results_text)):
    if full_results_text[i]['scores'][0] >= 0.5:
        results_text.append(full_results_text[i]['labels'][0])
        classified_text.append(full_results_text[i]['sequence'])

# save the results as a dataframe
df = pd.DataFrame()
df['Text'] = classified_text
df['Text Classification'] = results_text

df.to_csv(f"Amazon/{file_name}/classified.csv")
pickle.dump(candidates, open(f"Amazon/{file_name}/candidates.pkl", "wb"))

print(f'Size of data: {len(df)}')

print(f'end:{datetime.now()}')