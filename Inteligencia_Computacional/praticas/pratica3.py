from sklearnex import patch_sklearn 
import time
import sys
import os

patch_sklearn()

CSV_PATH = os.path.dirname(os.path.abspath(__file__))+ "/santander-customer-transaction-prediction"

import pandas as pd

df_test_kaggle = pd.read_csv(f"{CSV_PATH}/test.csv")
df_train = pd.read_csv(f"{CSV_PATH}/train.csv")
df_test_kaggle.head() #exibe as 5 primeiras linhas do dataframe

X = df_train.drop(columns=["ID_code", "target"]) #remove as colunas ID_code e target
y = df_train["target"] #iremos tentar prever a coluna target


X

df_test_kaggle

X_test_kaggle = df_test_kaggle.drop(columns=["ID_code"])

from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score, f1_score, make_scorer

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

X_train

def save_kaggle_solution(classifier, file_name):
    classifier.fit(X, y) # treina o classificador com todo conjunto de treino
    y_pred_kaggle = classifier.predict(X_test_kaggle) #prediz a classe (ou seja, a coluna target)
    df_test_kaggle["target"] = y_pred_kaggle #atribuindo as predições para o dataframe com os dados de teste. Cada linha receberá a sua respectiva predição.
    df_test_kaggle[["ID_code","target"]] #exibe as colunas que serão enviadas para o Kaggle
    df_test_kaggle[["ID_code","target"]].to_csv(file_name + ".csv", index=False) #salva as colunas que serão enviadas para o Kaggle em um arquivo csv

def avaliar_modelo_cv(classificador, X, y):
    f1_macro = make_scorer(f1_score, average='macro', zero_division=0)
    resultados = cross_validate(
        classificador,
        X,
        y,
        cv=10,
        scoring=["f1_macro", 'precision',"zero_division"],
        return_train_score=False
    )
    return resultados["test_score"].mean()

def avaliar_modelo_treino_teste(classificador, X_train, y_train, X_test, y_test):
    y_pred = classificador.predict(X_test)
    return f1_score(y_test, y_pred, average='macro')

#!unzip santander-customer-transaction-prediction.zip

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

classifier = DecisionTreeClassifier(random_state=0,max_depth=3) #instancia o classificador
#classifier = GaussianNB() #instancia o classificador
#classifier = KNeighborsClassifier() #instancia o classificador

""" classifier.fit(X_train, y_train) #treina o classificador
scores = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)

print(f"score f1  = {scores['test_f1_macro'].mean()}")

y_pred = classifier.predict(X_test) #prediz a classe (ou seja, a coluna target)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia árvore de decisão sem melhorias = {accuracy}") """


def print_decision_tree_f1_cross_fold(f1_score, altura_arvore):
  print(f"Cross Fold f1 árvore de decisão com melhorias Cross Fold = {f1_score}, altura arvore = {altura_arvore}")
  
def print_decision_tree_f1(f1_score, altura_arvore):
  print(f"f1 treino_teste árvore de decisão com melhorias = {f1_score}, altura arvore = {altura_arvore}")
  
start_time = time.time() #inicia o cronometro

altura_ranges = range(1, 6)
for altura_arvore in altura_ranges:
  classifier = DecisionTreeClassifier(random_state=0,max_depth=altura_arvore) #instancia o classificador
  classifier.fit(X_train, y_train) #treina o classificador
  cross_fold_score = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)
  f1_score_treino_teste = avaliar_modelo_treino_teste(classifier, X_train, y_train, X_test, y_test)
  
  print_decision_tree_f1_cross_fold(cross_fold_score["test_f1_macro"].mean(), altura_arvore)
  print_decision_tree_f1(f1_score_treino_teste, altura_arvore)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo de execução: {elapsed_time:.2f} segundos")

classifier = GaussianNB() #instancia o classificador
classifier.fit(X_train, y_train) #treina o classificador
cross_fold_score = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)
f1_score_treino_teste = avaliar_modelo_treino_teste(classifier, X_train, y_train, X_test, y_test)
print(f"f1 treino_teste Navie Bayes = {f1_score_treino_teste}")
print(f"Cross Fold f1 Navie Bayes = {cross_fold_score['test_f1_macro'].mean()}")

classifier = KNeighborsClassifier() #instancia o classificador
classifier.fit(X_train, y_train) #treina o classificador
cross_fold_score = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)
f1_score_treino_teste = avaliar_modelo_treino_teste(classifier, X_train, y_train, X_test, y_test)
print(f"f1 treino_teste KNN = {f1_score_treino_teste}")
print(f"Cross Fold f1 KNN = {cross_fold_score['test_f1_macro'].mean()}")

def print_knn_f1_cross_fold(f1_score, n_neighbors, weight, metric):
  print(f"Cross Fold f1 KNN = {f1_score}, n_neighbors = {n_neighbors}, weight = uniform, metric = minkowski")
  
def print_knn_f1(f1_score, n_neighbors, weight, metric):
    print(f"f1 treino_teste KNN = {f1_score}, n_neighbors = {n_neighbors}, weight = uniform, metric = minkowski")
  
for n_neighbors in range(2, 6):
    classifier = KNeighborsClassifier(n_neighbors=n_neighbors) #instancia o classificador
    classifier.fit(X_train, y_train) #treina o classificador
    cross_fold_score = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)
    f1_score_treino_teste = avaliar_modelo_treino_teste(classifier, X_train, y_train, X_test, y_test)
    
    print_knn_f1_cross_fold(cross_fold_score["test_f1_macro"].mean(), n_neighbors, "uniform", "minkowski")
    print_knn_f1(f1_score_treino_teste, n_neighbors, "uniform", "minkowski")
    
from sklearn.svm import LinearSVC
classifier = LinearSVC()
classifier.fit(X_train, y_train)
cross_fold_score = cross_validate(classifier, X_train, y_train, scoring=["f1_macro", 'precision'], cv=10)
f1_score_treino_teste = avaliar_modelo_treino_teste(classifier, X_train, y_train, X_test, y_test)


  