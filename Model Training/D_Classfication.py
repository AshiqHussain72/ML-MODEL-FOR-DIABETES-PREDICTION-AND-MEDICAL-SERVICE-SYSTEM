import numpy as np
import pandas as pd

df = pd.read_csv('diabetes.csv')
df.head() 
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
labels = df['Outcome'].values
features = df[list(columns)].values
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.30)
clf = RandomForestClassifier(n_estimators=1)
clf = clf.fit(X_train, y_train)
accuracy = clf.score(X_train, y_train)
print (accuracy*100)
accuracy = clf.score(X_test, y_test)
print (accuracy*100)
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

ypredict = clf.predict(X_train)
print ('\nTraining classification report\n', classification_report(y_train, ypredict))
print ("\n Confusion matrix of training \n", confusion_matrix(y_train, ypredict))
ypredict = clf.predict(X_test)
print ('\nTraining classification report\n', classification_report(y_test, ypredict))
print ("\n Confusion matrix of training \n", confusion_matrix(y_test, ypredict))