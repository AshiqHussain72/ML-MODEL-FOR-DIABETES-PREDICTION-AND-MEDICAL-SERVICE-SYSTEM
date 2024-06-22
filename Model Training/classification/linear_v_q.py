import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#-------------------

#loading the dataframe
df = pd.read_csv('D:/Python Run/HDFS_frame/classification/pima_indians_diabetes.txt')

#-------------------

#defining the columns 
df.columns =['No_pregnant', 'Plasma_glucose', 'Blood_pres', 'Skin_thick', 
             'Serum_insu', 'BMI', 'Diabetes_func', 'Age', 'Class']
#-------------------

#checking the dataframe
print(df.head())
print(df.dtypes)
print(df.shape) #(767, 9)

#identify nans
def num_missing(x):
  return sum(x.isnull())
#Applying per column:
print ("Missing values per column:")
print (df.apply(num_missing, axis=0),'\n') #no nans

#-------------------

#Apply the K nearest neighbour classifier

#split the data into training and testing datasets
X = np.array(df.drop(['Class'], axis = 1))
y = np.array(df['Class'])
X_train, X_test, y_train, y_test = train_test_split(X, y , test_size =0.5, 
                                                    random_state = 7)

#apply the knn method
Knn = KNeighborsClassifier(n_neighbors = 2)

#train the data
Knn.fit(X_train,y_train)

#test the data
accuracy = Knn.score(X_test, y_test)#this to see how accurate the algorithm is in terms 
#of defining the diabetes to be either 1 or 0
print('accuracy of the model is: ', accuracy) #0.73

