# 2022 SUTD DAI Term 4 Group 3
## Group Members

1. Abigail Tan Juan Hong
2. Chua Po Siang Bridget
3. Prabhakar Dhilahesh
4. Seetoh Jian Qing
5. Tan Rui Yang

# Project Description
This project is to identify the design recommendation for the **Apple Watch Series 7** in the sustainablity aspect by using Artificial Intelligence (AI).

We will be scraping data from three sources.
1. Google
2. Reddit
3. Amazon

# Google
We will be using Selenium to scrape the pages. We uses Google search to find out how the world talks about sustainability (since this project wanted to find design opportunity through sustainability).

Before we start, we need to download the chromedriver that fits your Google Chrome version by this [link](https://chromedriver.chromium.org/downloads). There is a provided chromedrive in the folder which can be used.

For the codes, we run these codes in sequence:
1. Data_Scraping.py
2. Analyze_Data.py
3. Classify_Data.py

## Data Scraping
Before we search for anything, users only need to change the *google_search* variable. After we run the code, Selenium will start scraping the webpages. The contents will be saved into a csv file for further analysis.

## Prepare and Analyze Data
Before we do any analyze, we will need to clean the data that we collected. The code will also create a word cloud to make us easier to look for the top words appeared. The words appeared more frequent means that the word is more related to the search terms that we want and it will be used as the labels for the classification for different platform.

# Reddit
Reddit is a popular public message board that has multiple threads online. Many of the comments are reasonably “high quality”- long opinionated statements about their experiences. We will use a library called *Praw* to scrape the data as it can help us scrape also the subreddits comments easily. Before we start scraping, we need to get an account for Reddit and follow this [page](https://praw.readthedocs.io/en/stable/#getting-started) to create the API. 

After everything is ready, we need to run these codes in sequence:
1. Scraping.py
2. Classifier.py
3. Classifier_Confusion_Matrix.py
4. Vader_Analysis.py
5. Vader_Confusion_Matrix.py

## Classification
To classify the data, we use the "zero-shot-classifier". To help us classify the data as a few labels that linked back to the result **(top words from above and from Google)**. 

After we classified the reviews, we only take in account of the reviews that have above 50% confident such that the reviews are better for further analyze according to the labels. Lastly, we will be saving the data into a csv file so that we can also read the file easier.

> If your computer/laptop has a Nvidia GPU, it is recommended to use the code that is left uncommented as using GPU runs much faster than CPU. Otherwise, use the commented line of code.

## Sentiment Analysis
We are using a model from nltk library called *vader*. While we are doing the sentiment analysis, we do not consider the labels for 'others' (if applicable) because they are not in consider in our design recommendation and supposingly most of them should not be user feedback according the product's design.

## Confusion Matrix
For confusion matrix, we will need to classify the reviews ourselves. To make our life easier, we random pick 20 reviews to check how is the accuracy. We will be using the confusion matrix from Scikit-learn library also to make our life easier.

### Sentiment Analysis
We will need to do the confusion matrix for each of the labels such that we can analyze how accurate that the AI classifies the components that we are giving recommendation to is good or bad.


# Amazon
We uses an Edge extension which can be found by this [link](https://chrome.google.com/webstore/detail/amazon-reviews-exporter-c/njlppnciolcibljfdobcefcngiampidm) to scrape the reviews. To use this extension, we need to find the product page that we want at Amazon (the extension is only usable on [Amazon](https://www.amazon.com/) for US).

For the codes, we run the codes in the sequence:
1. Prepare_Data.py
2. Analyze_Data.py
3. Classifier.py
4. Classification_Confusion_Matrix.py
5. Sentiment_Analysis.py
6. Sentiment_Confusion_Matrix.py

## Prepare Data
This code is to clean the reviews.

We need to have the data scraped by the extension mentioned above which is a csv file. We clean and translate the data into English for further analyze. While we are translating the data, we found that the reviews with less characters will have low quality. Therefore, we decided to filter out the reviews that are lesser than 15 characters. These reviews included: "good", "bad", "amazing thing" and etc.

> Note that the *file_name* variable is important when we are running our code. Make sure it is the file name of your scraped data (everything before .csv).

## Analyze Data
We uses wordcloud and also n-grams (at most n continuous sequence of words) to analyze the cleaned data. We will take the top 150 appeared words to find out what it the most mentioned things for the product. To get more useful top words, we will pay more attention on words that appeared as a phrase. such as "battery life", "heart rate" and etc.

> For the other codes, all of them works the same as Reddit's part. Therefore, we are not going to talk about it here again. 

# References
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
