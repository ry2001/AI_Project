import pandas as pd
from transformers import pipeline
import pickle
import re

def clean_text(text):                               # user defined function for cleaning text
    text = text.lower()                             # all lower case
    text = re.sub(r'\[.*?\]', ' ', text)            # remove text within [ ] (' ' instead of '')
    text = re.sub(r'\<.*?\>', ' ', text)            # remove text within < > (' ' instead of '')
    text = re.sub(r'http\S+', ' ', text)            # remove website ref http
    text = re.sub(r'www\S+', ' ', text)             # remove website ref www

    text = text.replace('€', 'euros')               # replace special character with words
    text = text.replace('£', 'gbp')                 # replace special character with words
    text = text.replace('$', 'dollar')              # replace special character with words
    text = text.replace('%', 'percent')             # replace special character with words
    text = text.replace('\n', ' ')                  # remove \n in text that has it

    text = text.replace('\'', '’')                  # standardise apostrophe
    text = text.replace('&#39;', '’')               # standardise apostrophe

    text = text.replace('’d', ' would')             # remove ’ (for would, should? could? had + PP?)
    text = text.replace('’s', ' is')                # remove ’ (for is, John's + N?)
    text = text.replace('’re', ' are')              # remove ’ (for are)
    text = text.replace('’ll', ' will')             # remove ’ (for will)
    text = text.replace('’ve', ' have')             # remove ’ (for have)
    text = text.replace('’m', ' am')                # remove ’ (for am)
    text = text.replace('can’t', 'can not')         # remove ’ (for can't)
    text = text.replace('won’t', 'will not')        # remove ’ (for won't)
    text = text.replace('n’t', ' not')              # remove ’ (for don't, doesn't)

    text = text.replace('’', ' ')                   # remove apostrophe (in general)
    text = text.replace('&quot;', ' ')              # remove quotation sign (in general)

    text = text.replace('cant', 'can not')          # typo 'can't' (note that cant is a proper word)
    text = text.replace('dont', 'do not')           # typo 'don't'

    text = re.sub(r'[^a-zA-Z0-9]', r' ', text)      # only alphanumeric left
    text = text.replace("   ", ' ')                 # remove triple empty space
    text = text.replace("  ", ' ')                  # remove double empty space
    return text

text = pd.read_csv("C:/Users/RY/Downloads/Telegram Desktop/Mood_lamp_all_comments.csv")
text = list(text['0'])

cleaned_text = []
for i in text:
    if isinstance(i,str):
        cleaned_text.append(clean_text(i))

candidates = ["brightness", "color", "controller", "others"] 

classifier = pipeline("zero-shot-classification", device=0)

full_results_text = []

for i in range(len(cleaned_text)):
    print(f'{i+1} of {len(cleaned_text)} done.')
    full_results_text.append(classifier(cleaned_text[i], candidate_labels = candidates))

classified_text = []
results_text = []

for i in range(len(full_results_text)):
    if full_results_text[i]['scores'][0] >= 0.5:
        results_text.append(full_results_text[i]['labels'][0])
        classified_text.append(full_results_text[i]['sequence'])

df = pd.DataFrame()
df['Text'] = classified_text
df['Text Classification'] = results_text

df.to_csv("classified.csv")