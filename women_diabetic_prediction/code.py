#importing Dependencies
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
#Load the dataset
diabetes=pd.read_csv("/content/diabetes (1).csv")
#First five values
diabetes.head()
#No of rows and columns of the dataset
diabetes.shape
#Statistical meausres of the data
diabetes.describe()
#0--->Non Diabetic
#1--->Diabetic
diabetes["Outcome"].value_counts()

#Standardise data
scaler=StandardScaler()
standardise_data=scaler.fit_transform(X)
#Prepare Standardise data
X=standardise_data
y=diabetes['Outcome']
#Split data
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,stratify=y,random_state=2)
#Model Training
model=svm.SVC(kernel='linear')
#Fit Model
model.fit(X_train,y_train)
#Model prediction for train data
x_train_predict=model.predict(X_train)
x_train_accuracy=accuracy_score(x_train_predict,y_train)
print("Accuracy on train data:",x_train_accuracy)
#Model prediction for test data
x_test_predict=model.predict(X_test)
x_test_accuracy=accuracy_score(x_test_predict,y_test)
print("Accuracy on test data:",x_test_accuracy)
#Building a Predictive system
input_data=(5,109,75,26,0,36,0.546,60)
input_data_as_array=np.asarray(input_data)
input_data_reshaped=input_data_as_array.reshape(1,-1)
#standardise the input data
std_data=scaler.transform(input_data_reshaped)

prediction=model.predict(std_data)

print(prediction[0])
if(prediction[0]==0):
  print("The person is not diabetic")
else:
  print("The person is diabetic")
