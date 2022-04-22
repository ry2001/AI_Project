from sklearn.metrics import confusion_matrix
import pandas as pd
import random
import numpy as np

df=pd.read_csv("D:\Coding Projects\Battery Comments.csv")      #insert csv where it's already labelled


# df=df.loc[df["Text Classification"]!="Others"]



y_true=[]
y_pred=[]
random_list= random.sample(range(0, len(df['Text Classification'])), 20)
print(random_list)

counter=0

df=df.reset_index()


                       

for x in random_list:
    y_pred.append(df['Text Classification'][x])

    
    print(df["Text"][x] + "--------> Positive or Negative?")
    my_input=input()
    
    counter+=1 
    

    if my_input=="p":
        y_true.append("Positive")
    if my_input=="n":
        y_true.append("Negative")
    # if my_input=="s":
    #     y_true.append("Strap")
    # if my_input=="o":
    #     y_true.append("Others")
    # else:
    #     y_true.append("Others")
    


    print(str(counter) + "/" + str(len(random_list)))


    

A= confusion_matrix(y_true, y_pred, labels=["Positive", "Negative"])
print(A)


accuracy= ((A[0,0] + A[1,1])/(np.sum(A)))*100

print(np.sum(A))



print("Accuracy is " + str(accuracy) + "%")