import time
import cx_Oracle
import psycopg2 as pg
from datetime import timedelta
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from multiprocessing.pool import ThreadPool
from matplotlib.pyplot import figure
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings('ignore')
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsClassifier 
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.python.client import device_lib
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.decomposition import PCA
import pickle

feature_cols = []
valData      = []
ingredients  = []

kfold         = 10

def postgresConnection():
    try:
        connection = pg.connect(
            host="localhost",
            user='postgres',
            password="Welcome123",
        )
        print('postgresConnection established...')
        return connection
    except Exception as e:
        print("Exception occurrred")
        print(str(e))

def getAllFeatures(colHeader = None):
    label = []
    labelDict = {}
    try:
        conn = postgresConnection()
        c = conn.cursor()
        if colHeader is None:
            sql = "select column_name from information_schema.columns where upper(TABLE_NAME) = 'VW_INGREDIENTS'"
            c.execute(sql)
            res = c.fetchall()            
            for row in res:
                label.append(row[0])
                labelKey = row[0]
                labelValue = labelKey.replace("_"," ")
                labelDict[labelKey] = labelValue
            return labelDict
        else:
            for item in colHeader:
                sql = "select column_name from information_schema.columns where upper(TABLE_NAME) = 'VW_INGREDIENTS' \
                and column_name = '"+item.replace(' ','_')+"'"
                #print(sql)
                c.execute(sql)
                res = c.fetchall()
                for row in res:
                    label.append(row[0])
                    labelKey = row[0]
                    labelValue = labelKey.replace("_"," ")
                    labelDict[labelKey] = labelValue
            return labelDict                
    except Exception as e:
        print("Exception occurrred in getAllFeatures")
        print(str(e))

def getPredictData(result,column_names,ingredients):
    global feature_cols
    global valData
    ls = []
    try:
        ketMetaData = set()
        #print(len(result))
        for item in result:
            dict = {}
            for val in range(len(item)):
                if item[val] == 1:
                    dict[column_names[val]] = 1
                    ketMetaData.add(column_names[val])
            ls.append(dict)
        
        #print(ls)
        keyList      = list(ketMetaData)
        feature_cols = keyList
        feature_cols.remove('healthy')
        feature_cols.remove('rnk')
        label_cols   = ['healthy']
        #preparing validation data
        valData = []
        for i in keyList:
            if i in ingredients:
                valData.append(1)
            else:
                valData.append(0)
        return valData
    except Exception as e:
        print("Exception occurrred in getPredictData")
        print(str(e))

def getModellingData(ingredientsDict):
    try:
        ingredients  = ingredientsDict.keys()
        fltr = ' = 1 or '.join(x for x in ingredients) + ' = 1'   
        conn = postgresConnection()
        curr = conn.cursor()
        sql = "with temp as ( select A.*,row_number() over (partition by healthy) as RNK from RECIPEDB.VW_INGREDIENTS A \
        where "+fltr+") SELECT * FROM TEMP where RNK <= 1000"
        print(sql)
        curr.execute(sql)
        column_names = [desc[0] for desc in curr.description]
        result = curr.fetchall()
        curr.close()
        conn.close()
        return {'column_names':column_names,'data':result}
    except Exception as e:
        print("Exception occurrred in getModellingData")
        print(str(e))

def mlModelling(df,algo):
    global kfold
    try:
        algorithm = ''
        if algo == 'LR':
            algorithm = 'Logistic Regression '
        elif algo == 'NB':
            algorithm = 'Naive Bayes '
        elif algo == 'SVM':
            algorithm = 'Support Vector Machine '
        elif algo == 'KNN':
            algorithm = 'K Nearest Neigbor '

        X = df[feature_cols]
        y = df['healthy']
        
        sc = StandardScaler()
        mms = MinMaxScaler()
        print('---------------------------')
        #sc = StandardScaler()
        X_scaled = sc.fit_transform(X)
        ############################################
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,shuffle=True, random_state=0)
        print(algorithm + 'without PCA')
        print('---------------------------')        
        print('Input Features:')
        print(ingredients)
        print('---------------------------')        
        print('Shape of training | test feature set:')
        print(X_train.shape,'      |',X_test.shape)
        
        if algo == 'LR':
            clf = LogisticRegression()
        elif algo == 'NB':
            clf = GaussianNB()
        elif algo == 'SVM':
            clf = SVC(C = 1e5, kernel = 'linear')
        elif algo == 'KNN':
            clf = KNeighborsClassifier(n_neighbors=3) 
        # Train the model
        clf.fit(X_train, y_train)
        
        # Save the model
        algorithm = algorithm.replace(' ','_')
        modleFileName = algorithm+'_pickle.pk1'
        with open(modleFileName, 'wb') as file:  
            pickle.dump(clf, file)
            
        # Make predictions
        y_pred = clf.predict(X_test) # Predictions
        y_true = y_test # True values
        
        print('---------------------------')
        print("Train accuracy:", np.round(accuracy_score(y_train, 
                                                        clf.predict(X_train)), 2))
        print("Test accuracy:", np.round(accuracy_score(y_true, y_pred), 2))
        
        #Predict Class Labels
        predicted = clf.predict(X_test)
        # Make the confusion matrix
        plt.clf()
        cf_matrix = metrics.confusion_matrix(y_test, predicted)

        sns.heatmap(cf_matrix, annot=True, cmap='Oranges')
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('True', fontsize=12)
        
        #Classification Report
        print('---------------------------')
        print('Classification Report')
        print(metrics.classification_report(y_test, y_pred))
        print('---------------------------')
        
        #Model Accuracy
        print('Model Accuracy',clf.score(X_test,y_test))
        print('---------------------------')
        
        #Cross-testation
        cross_val = cross_val_score(clf, X, y, scoring='accuracy', cv=kfold)
        print('Cross-validation : ',cross_val)
        print('---------------------------')
        print('Cross-Validation mean : ',round(cross_val.mean(),2))
        print('---------------------------')
        print('Confusion Matrix : ')
        print('---------------------------')
        diet_Pred = clf.predict([valData])
        fType = ''
        if diet_Pred == 1:
            fType = 'Healthy'
        else:
            fType = 'Unealthy'
        print('Prediction for the food with input ingrdeient feature:',fType)        
        
    except Exception as e:
        print("Exception occurrred in mlModelling")
        print(str(e))
        raise
        
def getPCAnumber(df):
    try:
        X = df[feature_cols]
        y = df['healthy']
        pca = PCA(n_components=None)
        #pca.fit(X_scaled)
        pca.fit(X)
        # Get the eigenvalues
        print("Eigenvalues:")
        print(pca.explained_variance_)
        
        # Get explained variances
        print("Variances (Percentage):")
        print(pca.explained_variance_ratio_ * 100)
        
        # Make the scree plot
        plt.plot(np.cumsum(pca.explained_variance_ratio_ * 100))
        plt.xlabel("Number of components (Dimensions)")
        plt.ylabel("Explained variance (%)")
        plt.show()
        
    except Exception as e:
        print("Exception occurrred in getPCAnumber")
        print(str(e))
        
def mlModellingPCA(df,algo,pc):
    global kfold
    try:
        algorithm = ''
        if algo == 'LR':
            algorithm = 'Logistic Regression '
        elif algo == 'NB':
            algorithm = 'Naive Bayes '
        elif algo == 'SVM':
            algorithm = 'Support Vector Machine '
        elif algo == 'KNN':
            algorithm = 'K Nearest Neigbor '
        

        X = df[feature_cols]
        y = df['healthy']
        
        # Apply PCA
        pca = PCA(n_components=pc)
        #X_pca = pca.fit_transform(X_scaled)
        X_pca = pca.fit_transform(X)
        
        # Get the transformed dataset
        X_pca = pd.DataFrame(X_pca)
        print(X_pca.head())
        print("\nSize: ")
        print(X_pca.shape)
        
        sc = StandardScaler()
        mms = MinMaxScaler()
        print('---------------------------')
        ############################################
        X_train_pca, X_test_pca, y_train, y_test = train_test_split(X_pca, y, test_size=0.20,shuffle=True, random_state=0)
        print(algorithm + ' with PCA')
        print('---------------------------')        
        print('Input Features:')
        print(ingredients)
        print('---------------------------')        
        print('Shape of training | test feature set:')
        print(X_train_pca.shape,'      |',X_test_pca.shape)
        
        if algo == 'LR':
            clf = LogisticRegression()
        elif algo == 'NB':
            clf = GaussianNB()
        elif algo == 'SVM':
            clf = SVC(C = 1e5, kernel = 'linear')
        elif algo == 'KNN':
            clf = KNeighborsClassifier(n_neighbors=3) 
        # Train the model
        clf.fit(X_train_pca, y_train)
        
        # Make predictions
        y_pred = clf.predict(X_test_pca) # Predictions
        y_true = y_test # True values
        
        print('---------------------------')
        print("Train accuracy:", np.round(accuracy_score(y_train, 
                                                        clf.predict(X_train_pca)), 2))
        print("Test accuracy:", np.round(accuracy_score(y_true, y_pred), 2))
        
        #Predict Class Labels
        predicted = clf.predict(X_test_pca)

        plt.clf()
        cf_matrix = metrics.confusion_matrix(y_test, predicted)

        sns.heatmap(cf_matrix, annot=True, cmap='Oranges')
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('True', fontsize=12)
        
        #Classification Report
        print('---------------------------')
        print('Classification Report')
        print(metrics.classification_report(y_test, y_pred))
        print('---------------------------')
        
        #Model Accuracy
        print('Model Accuracy',clf.score(X_test_pca,y_test))
        print('---------------------------')

        #Cross-testation
        cross_val = cross_val_score(clf, X_pca, y, scoring='accuracy', cv=kfold)
        print('Cross-validation : ',cross_val)
        print('---------------------------')
        print('Cross-Validation mean : ',round(cross_val.mean(),2))
        print('---------------------------')
        print('Confusion Matrix : ')
        print('---------------------------')
        #diet_Pred = clf.predict([valData])
        #fType = ''
        #if diet_Pred == 1:
        #    fType = 'Healthy'
        #else:
        #    fType = 'Unealthy'
        #print('Prediction for the food with input ingrdeient feature:',fType)        
        
    except Exception as e:
        print("Exception occurrred in mlModellingPCA")
        print(str(e))
        
def main():
    global ingredients
    try:
        features     = []
        ingredients  = ['olive oil','onion','white wine','anchovy','tomato','garlic','basil','oregano',
                'fish','orange peel','white bread','apple','lemon juice','olive oil','black pepper']
                
        ############################################
        
        ingredientsDict = getAllFeatures(ingredients)
        print(list(ingredientsDict.keys()))
        
        ############################################
        
        modellingData = getModellingData(ingredientsDict)
        
        ############################################
        
        df = pd.DataFrame(modellingData['data'], columns=modellingData['column_names'])
        df = df.drop(columns=['rnk'])
        #print(df.describe())
        
        ###########################################
        
        #prepare the predicts data
        column_names = modellingData['column_names']
        data = modellingData['data']
        getPredictData(data,column_names,ingredients)

        #############################################
        
        #mlModelling(df,'LR')   # ['LR','NB','SVM','KNN']
        #print(valData)
        
        #############################################
        
        #getPCAnumber(df)
        #mlModellingPCA(df,'LR',150)
        
        #############################################
        
    except Exception as e:
        print("Exception occurred",str(e))    
if __name__ == '__main__':
    if main():
        True
    else:
        False
