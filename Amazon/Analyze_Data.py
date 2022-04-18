# The code to do a quick analyze about the words mentioned in the reviews

import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from nltk.util import everygrams
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")


# to analyze how the data should work
e_grams_max = 3          # Maximum length of every-grams (i.e. 1 = single word)
e_grams_cut = 150        # Number of top words/every-grams to be analysed

# importing the data required for this code
file_name = pd.read_pickle('Amazon/file_name.pkl')
all_reviews = pd.read_pickle(f"Amazon/{file_name}/all_reviews.pkl")
stop = pd.read_pickle(f"Amazon/{file_name}/stop_words.pkl")

# initializing stopwords
all_stopwords = stopwords.words('english')
all_stopwords.extend(stop)
STOPWORDS.update(all_stopwords)

# create a wordcloud to show how the words appears in the data
print("Creating WordClouds...")
wc = WordCloud(stopwords=STOPWORDS, background_color="white", colormap="Dark2", collocations=False,
               max_font_size=150, include_numbers=True, random_state=42)  # add "max_words=10" to limit number of words (optional)
fig2 = plt.figure(figsize=(8, 5))

if len(all_reviews[0]) != 0:     # WordCloud needs at least one word
    wc.generate(all_reviews[0])
else:
    wc.generate("empty")

# plot wordcloud
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(file_name, fontsize=10)
plt.savefig(f"Amazon/{file_name}/WordCloud.png")

print("Finding top words...")
top_words = []
top = []

# count for all possible combinations of words appeared in the reviews
all_reviews[0] = " ".join(word for word in all_reviews[0].split() if word not in all_stopwords)
e_grams_counts = Counter(everygrams(all_reviews[0].split(), max_len=e_grams_max))
e_grams_most = e_grams_counts.most_common(e_grams_cut)

# to have higher quality results, we will take the top words that is a phrase, more than one words.
for i,j in enumerate(e_grams_most):
    if len(j[0]) == 1:
        pass
    else:
        top.append([" ".join(e_grams_most[i][0]), e_grams_most[i][1]])
top_words.append(top.copy())

pickle.dump(top_words, open(f"Amazon/{file_name}/top_words.pkl", "wb"))