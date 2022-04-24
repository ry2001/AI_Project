import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.corpus import stopwords

search_term = pd.read_pickle("Reddit/search_term.pkl")
df = pd.read_csv(f"Reddit/{search_term}_classified.csv")
candidates = pd.read_pickle("Reddit/candidates.pkl")

sentiments = {}
for i in candidates:
    if i != 'others':
        sentiments[i] = {"Positive": [] , "Negative": []}

sid = SentimentIntensityAnalyzer()

stop_words = set(stopwords.words("english"))
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

no_punct = ""

positive_text = []
negative_text = []
sentiment_results = []

for i in range(len(df["Text Classification"])):
    text = df["Text"][i].lower()

    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char

    if df["Text Classification"][i] in sentiments.keys():
        scores = sid.polarity_scores(text)
        if scores['compound']> 0.5:
            sentiments[df["Text Classification"][i]]["Positive"].append(text)
            sentiment_results.append('positive')
        else: 
            sentiments[df["Text Classification"][i]]["Negative"].append(text)
            sentiment_results.append('negative')
    else:
        sentiment_results.append('Not Applicable')

for i in sentiments.keys():
    for j in sentiments[i]:
        print(f'For {i}, there are {len(sentiments[i][j])} {j} Sentiments')

# save data into a dataframe
df2 = df[['Text', 'Text Classification']]
df2['Sentiment'] = sentiment_results

for i in sentiments.keys():
    ndf = df2[df2['Text Classification'] == i].reset_index(drop = True)
    ndf.to_csv(f"Reddit/{search_term}_{i}_sentiments.csv")