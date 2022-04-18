from sklearn.metrics import confusion_matrix
import pandas as pd
import random
import numpy as np

# import the files needed
file_name = pd.read_pickle("Amazon/file_name.pkl")
df = pd.read_csv(f"Amazon/{file_name}/classified.csv")               # insert csv where it's already labelled
candidates = pd.read_pickle(f"Amazon/{file_name}/candidates.pkl")    # labels

# label for the input
def label(candidates):
    lab = {}
    rev_lab = {}
    for i in candidates:
        if i[0] not in rev_lab.keys():
            lab[i] = i[0]
            rev_lab[i[0]] = i
        # to avoid collision
        else:
            lab[i] = i[0:2]
            rev_lab[i[0:2]] = i
    return lab, rev_lab

# function to check valid inputs
def check_input():
    my_input = input()
    labels, _ = label(candidates)
    if my_input not in labels.values():
        my_input = check_input()
    return my_input

labels, rev_labels = label(candidates)

y_true = []
y_pred = []
random_list = random.sample(range(0, len(df['Text Classification'])), 20)

counter = 0

# to show what to input
txt = ''
for key,val in labels.items():
    txt += f'{key}({val}) '

# do the classification manually
for x in random_list:
    y_pred.append(df['Text Classification'][x])
    print(df["Text"][x] + "--------> " + txt)
    my_input = check_input()
    counter += 1 
    y_true.append(rev_labels[my_input])
    print(str(counter) + "/" + str(len(random_list)))

cm = confusion_matrix(y_true, y_pred, labels = candidates)

tp = 0

# find the number of true positives
for i in range(len(cm)):
    for j in range(len(cm)):
        if i == j:
            tp += cm[i][j]

# calculate the accuracy
accuracy = (tp / (np.sum(cm))) * 100

print("Confusion Matrix:")
print(cm)

print(f"Accuracy is {accuracy}%")