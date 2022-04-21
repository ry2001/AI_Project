import pandas as pd
from transformers import pipeline

search = pd.read_pickle("Google/search_word.pkl")
text = pd.read_pickle(f"Google/{search}/clean_text.pkl")

candidates = ["sustainabile", "size", "colours", "others"]

classifier = pipeline("zero-shot-classification", device = 0) # if have gpu
# classifier = pipeline("zero-shot-classification")           # if no gpu

full_results_text = []

# put the results into a list
for i in text:
    full_results_text.append(classifier(i, candidate_labels = candidates))

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

df.to_csv(f"Google/{search}/classified.csv")