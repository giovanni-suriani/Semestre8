import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
import time


import sys
import os

CSV_PATH = os.path.dirname(os.path.abspath(__file__))+ "/santander-customer-transaction-prediction"

df_test_kaggle = pd.read_csv(f"{CSV_PATH}/test.csv")
df_train = pd.read_csv(f"{CSV_PATH}/train.csv")
df_test_kaggle.head() #exibe as 5 primeiras linhas do dataframe

X_train = df_train.drop(columns=["ID_code", "target"]) #remove as colunas ID_code e target
y_train = df_train["target"] #iremos tentar prever a coluna target

X_test_kaggle = df_test_kaggle.drop(columns=["ID_code"])

# Splitting the training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.3, random_state=42)


#!unzip santander-customer-transaction-prediction.zip



classifier = DecisionTreeClassifier(random_state=0,max_depth=3) #instancia o classificador
classifier.fit(X_train, y_train) #treina o classificador
#y_pred = classifier.predict(X_test) #prediz a classe (ou seja, a coluna target)
#
## Calcula a acurácia
#accuracy = accuracy_score(y_test, y_pred)
#print(f"Acurácia: decision tree =  {accuracy:.2f}") #exibe a acurácia
#
#classifier = GaussianNB()
#classifier.fit(X_train, y_train) #treina o classificador
#y_pred = classifier.predict(X_test) #prediz a classe (ou seja, a coluna target)
## Calcula a acurácia
#accuracy = accuracy_score(y_test, y_pred)
#print(f"Acurácia: Navie Bayes = {accuracy:.2f}") #exibe a acurácia


def print_knn_accurracy(y_pred, n_neighbors, weight, metric):
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do knn: {accuracy}, utilizando n_neighbors: {n_neighbors}, weight: {weight}, metric: {metric}") #exibe a acurácia
# KNN

def save_kaggle_solution(classifier, file_name):
    y_pred_kaggle = classifier.predict(X_test_kaggle) #prediz a classe (ou seja, a coluna target)
    df_test_kaggle["target"] = y_pred_kaggle #atribuindo as predições para o dataframe com os dados de teste. Cada linha receberá a sua respectiva predição.
    df_test_kaggle[["ID_code","target"]] #exibe as colunas que serão enviadas para o Kaggle
    df_test_kaggle[["ID_code","target"]].to_csv(file_name + ".csv", index=False) #salva as colunas que serão enviadas para o Kaggle em um arquivo csv
    
save_kaggle_solution(classifier, "solucao-2025") #salva a solução para o Kaggle


#df_test_kaggle["target"] = predictions
#
#df_test_kaggle[["ID_code","target"]] #exibe as colunas que serão enviadas para o Kaggle
#df_test_kaggle[["ID_code","target"]].to_csv("solucao-2025.csv", index=False)#salva as colunas que serão enviadas para o Kaggle em um arquivo csv



""" classifier = KNeighborsClassifier()
kneighbors_parameters = {
    'n_neighbors': [3, 4, 5, 6],
    'weights': ['uniform', 'distance'],
    'metric': ['minkowski','euclidean']
}

for n_neighbors in kneighbors_parameters['n_neighbors']:
    for weight in kneighbors_parameters['weights']:
        for metric in kneighbors_parameters['metric']:
            
            start_time = time.time() #inicia o cronometro
            classifier = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weight, metric=metric)
            classifier.fit(X_train, y_train) #treina o classificador
            y_pred = classifier.predict(X_test) #prediz a classe (ou seja, a coluna target)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Tempo de execução: {elapsed_time:.2f} segundos")
            print_knn_accurracy(y_pred, n_neighbors, weight, metric) #mostra a precisao para cada configuracao """

