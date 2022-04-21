import pandas as pd
from cleantext import clean
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from nltk.util import everygrams
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

stop = ["wa", "doe", "ha", "video", "one",
        "subscribe", "channel", "watch",
        "watching", "thanks", "thank", 
        'washer','washing', 'buy', 'hai', 'po', 'sa',
         'ko', 'bah', 'yung', 'please', 'think', 'felt', 'would', 'first',
         'amazon', 'machine', 'baat', 'bekar', 'yen', 'bro', 
         'kha', 'milga', 'yh', 'kiya', 'bhi','se', 'ye','sustainable', 'sustainability','building']      # Add stopwords (lower case)

all_stopwords = stopwords.words('english')  # set english
all_stopwords.extend(stop)                  # and extend with 'stop' above

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

def combine_text(list_of_text):
    combined_text = ' '.join(list_of_text)
    return combined_text

e_grams_max = 3          # Maximum length of every-grams (i.e. 1 = single word)
e_grams_cut = 50         # Number of top words/every-grams to be analysed (for a video)

search = pd.read_pickle("Google/search_word.pkl")

df = pd.read_pickle(f"Google/{search}/content.pkl")
for i in range(len(df)):
    df[i] = clean(df[i], no_emoji = True)

for val in df:
    val = filter(None, val)

sentences = []
data = []

for website in df:
    sentence = website.strip().split(',')
    if sentence != ['']:
        sentences.append(sentence)

for i in range(len(sentences)):
    clean_sentence = clean_text(sentences[i][0])                                   
    data.append(clean_sentence)                  # overwrite with clean_text function
    tokens = nltk.tokenize.TreebankWordTokenizer().tokenize(clean_sentence)  # each word as a token
    for k in range(len(tokens)):
        tokens[k] = nltk.stem.WordNetLemmatizer().lemmatize(tokens[k])      # stem each token
    data[i] = " ".join(tokens)   # join stemmed tokens back

cleaned_data = []
for i in data:
    i = i.strip()
    if i != '':
        cleaned_data.append(i)

data_clean = combine_text(cleaned_data)

words = len(data_clean.split())

# create a wordcloud to show how the words appears in the data
print("Creating WordClouds...")
wc = WordCloud(stopwords=STOPWORDS, background_color="white", colormap="Dark2", collocations=False,
               max_font_size=150, include_numbers=True, random_state=42)  # add "max_words=10" to limit number of words (optional)
fig2 = plt.figure(figsize=(8, 5))

if len(data_clean) != 0:     # WordCloud needs at least one word
    wc.generate(data_clean)
else:
    wc.generate("empty")

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(search, fontsize=10)
plt.savefig(f"Google/{search}/WordCloud.png")
plt.show()

print("Finding top words...")
top_words = []      # list of top words by video
top = []            # list of top words in each video

data_clean = " ".join(word for word in data_clean.split() if word not in all_stopwords)
e_grams_counts = Counter(everygrams(data_clean.split(), max_len=e_grams_max))
e_grams_most = e_grams_counts.most_common(e_grams_cut)
print(e_grams_most)

for j in range(len(e_grams_most)):
    top.append([" ".join(e_grams_most[j][0]), e_grams_most[j][1]])
top_words.append(top.copy())

pickle.dump(top_words, open(f"Google/{search}/top_words.pkl", "wb"))
pickle.dump(cleaned_data, open(f"Google/{search}/clean_text.pkl", "wb"))