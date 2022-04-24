# import nltk                       # only use for the first time
# nltk.download('vader_lexicon')    # only use for the first time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# import files that needed
file_name = pd.read_pickle("Amazon/file_name.pkl")
df = pd.read_csv(f"Amazon/{file_name}/classified.csv")
candidates = pd.read_pickle(f"Amazon/{file_name}/candidates.pkl")

# to store the analysis results
sentiments = {}
for i in candidates:
    if i != 'others':
        sentiments[i] = {"Positive": [] , "Negative": []}

# initialize model
sid = SentimentIntensityAnalyzer()

positive_text = []
negative_text = []
sentiment_results = []

# do sentiment analysis for all labels except for 'others'
for i in range(len(df["Text Classification"])):
    text = df["Text"][i]

    # all labels except 'others'
    if df["Text Classification"][i] in sentiments.keys():
        scores = sid.polarity_scores(text)
        if scores["compound"] > 0.05:
            sentiments[df["Text Classification"][i]]["Positive"].append(text)
            sentiment_results.append('positive')
        else:
            sentiments[df["Text Classification"][i]]["Negative"].append(text)
            sentiment_results.append('negative')
    # we are not considering 'others'
    else:
        sentiment_results.append('Not Applicable')

# to show number of positive and negative results for each label
for i in sentiments.keys():
    for j in sentiments[i]:
        print(f'For {i}, there are {len(sentiments[i][j])} {j} Sentiments')

# save data into a dataframe
df2 = df[['Text', 'Text Classification']]
df2['Sentiment'] = sentiment_results

for i in sentiments.keys():
    ndf = df2[df2['Text Classification'] == i].reset_index(drop = True)
    ndf.to_csv(f"Amazon/{file_name}/{i}_sentiments.csv")