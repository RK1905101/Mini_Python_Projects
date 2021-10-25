# Load libraries
import numpy as np
import pandas as pd
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier  # import the classifier

df = pd.read_csv("Book_Restaurant_Dataset.csv", header=None)


string_to_int = preprocessing.LabelEncoder()  # encode your data
df = df.apply(string_to_int.fit_transform)  # fit and transform it
# To divide our data into attribute set and Label:

X = df.iloc[0:10]  # contains the attribute
y = df.iloc[10]  # contains the label

# To divide our data into training and test sets:

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# perform training

classifier = DecisionTreeClassifier(criterion="entropy")  # create a classifier object
classifier.fit(X_train, y_train)  # fit the classifier with X and Y data
# Predict the response for test dataset
y_pred = classifier.predict(X_test)
print(y_pred)
pred = classifier.predict([[0, 1, 0, 1]])
print(pred)

# Model Accuracy, how often is the classifier correct?


print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
