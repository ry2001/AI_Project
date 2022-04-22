import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import random
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist

df=pd.read_csv("D:\Coding Projects\Apple_Labelled_Battery, Watch_Face, Strap.csv")  

Components=["Battery", "Watch Face", "Strap"]
Components_Sentiment={"Battery":{"Positive": [] , "Negative": []}, "Watch Face":{"Positive": [] , "Negative": []}, "Strap":{"Positive": [] , "Negative": []}}



sid = SentimentIntensityAnalyzer()
stop_words=set(stopwords.words("english"))
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

lem=WordNetLemmatizer()

no_punct=""

positive_text=[]
negative_text=[]

for i in range(len(df["Text Classification"])):
    text= df["Text"][i].lower()

    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char

    

    
    if df["Text Classification"][i] in Components:

        scores=sid.polarity_scores(text)

        if df["Text Classification"][i] == "Battery":

            

            if scores['compound']> 0.5:
                positive_text.append(text)
                Components_Sentiment["Battery"]["Positive"].append(text)
                


            else: 
                Components_Sentiment["Battery"]["Negative"].append(text)
                negative_text.append(text)

        if df["Text Classification"][i] == "Watch Face":
            
            if scores['compound']> 0.5:
                Components_Sentiment["Watch Face"]["Positive"].append(text)
            else: 
                Components_Sentiment["Watch Face"]["Negative"].append(text)

        if df["Text Classification"][i] == "Strap":
            
            if scores['compound']> 0.5:
                Components_Sentiment["Strap"]["Positive"].append(text)
            else: 
                Components_Sentiment["Strap"]["Negative"].append(text)



Battery_Positive= len(Components_Sentiment["Battery"]["Positive"])
Battery_Negative=len(Components_Sentiment["Battery"]["Negative"])
WatchFace_Positive= len(Components_Sentiment["Watch Face"]["Positive"])
WatchFace_Negative=len(Components_Sentiment["Watch Face"]["Negative"])
Strap_Positive= len(Components_Sentiment["Strap"]["Positive"])
Strap_Negative=len(Components_Sentiment["Strap"]["Negative"])



print(f"\nFor batteries: \n No. of Positive Sentiments is {Battery_Positive}. \n No. of Negative Sentiments is {Battery_Negative}\n ") 
print(f"\nFor Watch Face: \n No. of Positive Sentiments is {WatchFace_Positive}. \n No. of Negative Sentiments is {WatchFace_Negative}\n ")
print(f"\nFor Strap: \n No. of Positive Sentiments is {Strap_Positive}. \n No. of Negative Sentiments is {Strap_Negative}\n ")

positive_sentiment=pd.DataFrame(Components_Sentiment["Battery"]["Positive"])
negative_sentiment=pd.DataFrame(Components_Sentiment["Battery"]["Negative"])

Combined_sentiment=pd.concat([positive_sentiment, negative_sentiment], axis=1)
Combined_sentiment.columns=['Positive', "Negative"]



Combined_sentiment.to_csv("D:\Coding Projects\Battery Comments.csv")
# for i in Components_Sentiment["Battery"]["Negative"]:
#     print(f"sentence is: {i}\n\n\n")
# Positive_words=[]
# Punctuation=[",", ".", "!", "/", ')', '(', "'", "?"]
# for sentiment in Components_Sentiment["Watch Face"]["Negative"]:
#     tokenized_word=word_tokenize(sentiment)

#     for words in tokenized_word:
#             if words not in stop_words and words not in Punctuation:
#                 Positive_words.append(lem.lemmatize(words))


# fdist = FreqDist(Positive_words).most_common(50)

# print(fdist)




                

        
    


