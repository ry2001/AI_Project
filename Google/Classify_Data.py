import pandas as pd
from transformers import pipeline
import pickle

search = pd.read_pickle("Google/search_word.pkl")
text = pd.read_pickle(f"Google/{search}/clean_text.pkl")

candidates = ["sustainabile", "size", "colours", "others"] 

classifier = pipeline("zero-shot-classification")

class_text = []
full_results = []

for i in range(len(text)):
    try:
        full_results.append(classifier(text[i], candidate_labels=candidates))
        class_text.append(text[i])
    except:
        print(f'Error:{text[i]} at {i} of {len(text)}')

results = []

for i in range(len(full_results)):
    results.append(full_results[i]['labels'][0])

pickle.dump(class_text,open(f"Google/{search}/classified_text.pkl", "wb"))
pickle.dump(full_results,open(f"Google/{search}/results.pkl", "wb"))

df = pd.DataFrame()
df['Text'] = class_text
df['Classification'] = results

df.to_csv(f"Google/{search}/classified.csv")