# This is the first code to run
# to prepare data for analyzing

import os
from cleantext import clean
import pickle
import pandas as pd
import re
# import nltk                   # only use for the first time
# nltk.download('stopwords')    # only use for the first time
# nltk.download('wordnet')      # only use for the first time
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator


# create a list of stopwords
stop = ["wa", "doe", "ha", "video", "one",
        "subscribe", "channel", "watch", "la", "leh" ,"de",
        "watching", "thanks", "thank", "apple", "series", "watch", "fitbit"]


# initialize stopwords and extend with the list of stopwords created above
all_stopwords = stopwords.words('english')  # set english
all_stopwords.extend(stop)

# file name of the data
file_name = 'Apple'

# read and extract data that is needed
data = pd.read_csv(f"Amazon/{file_name}.csv")

# define functions
# to combine a list of text into a single string
def combine_text(list_of_text):
    combined_text = ' '.join(list_of_text)
    return combined_text

# to clean the text
def clean_text(text):
    text = text.lower()                             # all lower case
    text = re.sub(r'\[.*?\]', ' ', text)            # remove text within [ ] (' ' instead of '')
    text = re.sub(r'\<.*?\>', ' ', text)            # remove text within < > (' ' instead of '')
    text = re.sub(r'http\S+', ' ', text)            # remove website ref http
    text = re.sub(r'www\S+', ' ', text)             # remove website ref www

    text = text.replace('€', 'euros')               # replace special character with words
    text = text.replace('£', 'gbp')                 # replace special character with words
    text = text.replace('$', 'dollar')              # replace special character with words
    text = text.replace('%', 'percent')             # replace special character with words
    text = text.replace('\n', '')                   # remove \n in text that has it

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
    text = text.replace("-", ' ')                   # remove hyphen
    text = text.replace("   ", ' ')                 # remove triple empty space
    text = text.replace("  ", ' ')                  # remove double empty space
    return text

# review cleaning
for i in range(len(data)):
    if isinstance(data.text.loc[i],str):                        # if the comment is not 'nan'
        data.text.loc[i] = clean_text(clean(data.text.loc[i],no_emoji = True))

# create a copy of review
cleaned_data = data[['text']].dropna().reset_index(drop = True)

# initialize to store all the translated reviews (Amazon will have different language)
translated = []

# iterate through all reviews and translate them
for i in range(len(cleaned_data)):
    # we notice that there will have a lot of reviews that are not contributing and the limitation of the Google Translator
    # therefore, we only translate all reviews that are less than 5000 characters
    # and also discard all reviews that are less than 15 characters (e.g. good, bad, etc.)
    if len(cleaned_data.text.loc[i]) < 5000 and len(cleaned_data.text.loc[i]) > 15:
        translated.append(GoogleTranslator(source='auto', target='en').translate(cleaned_data.text.loc[i]))
        print(f'{i} out of {len(cleaned_data)} done.')

# convert the list of reviews into dataframe
translated_data = pd.DataFrame(translated, columns = ['text']).dropna().reset_index()

# combine all reviews into a single string
all_reviews = []
all_reviews.append(combine_text(translated))

# organize cleaned data
data_clean = pd.DataFrame(all_reviews, columns=['comments'])

# create folder with file_name in Amazon folder if it does not exist to store files
if not os.path.exists(f"Amazon/{file_name}"):
    os.makedirs(f"Amazon/{file_name}")

# save datas to use later or reference
pickle.dump(file_name,open("Amazon/file_name.pkl", "wb"))
pickle.dump(translated, open(f"Amazon/{file_name}/translated.pkl", "wb"))
pickle.dump(stop, open(f"Amazon/{file_name}/stop_words.pkl", "wb"))
pickle.dump(all_reviews, open(f"Amazon/{file_name}/all_reviews.pkl", "wb"))