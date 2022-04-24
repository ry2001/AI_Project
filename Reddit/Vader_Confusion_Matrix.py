from sklearn.metrics import confusion_matrix
import pandas as pd
import random
import numpy as np

# import files needed
search_term = pd.read_pickle("Reddit/search_term.pkl")
candidates = pd.read_pickle("Reddit/candidates.pkl")

# we are only dealing with positive and negative labels
res = ['positive', 'negative']

# label for the input
def label(candidates):
    lab = {}
    rev_lab = {}
    for i in candidates:
        if i[0] not in rev_lab.keys():
            lab[i] = i[0]
            rev_lab[i[0]] = i
        else:
            lab[i] = i[0:2]
            rev_lab[i[0:2]] = i
    return lab, rev_lab

# function to check valid inputs
def check_input():
    my_input = input()
    labels, _ = label(res)
    if my_input not in labels.values():
        my_input = check_input()
    return my_input

labels, rev_labels = label(res)

# for all labels except for 'others'
# do the classification manually
for i in candidates:
    if i != 'others':
        print(f'Confusion Matrix for {i}:')
        df = pd.read_csv(f"Reddit/{search_term}_{i}_sentiments.csv")
        y_true = []
        y_pred = []
        random_list = random.sample(range(0, len(df['Text Classification'])), 20)
        counter = 0

        txt = ''
        for key,val in labels.items():
            txt += f'{key}({val}) '

        for x in random_list:
            y_pred.append(df['Sentiment'][x])
            print(df["Text"][x] + "--------> " + txt)
            my_input = check_input()
            counter += 1
            y_true.append(rev_labels[my_input])
            print(str(counter) + "/" + str(len(random_list)))

        cm = confusion_matrix(y_true, y_pred, labels = res)
        tp = 0

        for i in range(len(cm)):
            for j in range(len(cm)):
                if i == j:
                    tp += cm[i][j]

        accuracy = (tp / (np.sum(cm))) * 100

        print("Confusion Matrix:")
        print(cm)

        print(f"Accuracy is {accuracy}%")