#!/usr/bin/env python

##
# @mainpage Heart Failure Prediction Project
#
# @section description_main Description
# A program that compares multiple ML models which determine the probability
# of heart failure in different people.
#
# @section notes_main Notes
# Models tested: Support Vector Machines, KNN, Logistic Regression,
# Random Forest, ANN, Decision Tree, xgboost, catboost.
#
# @section author_main Author(s)
# - Created by [Your Name] on [Date].
# - Modified by [Your Name] on [Date].
#
# @section license_main License
# Copyright (c) 2023 UTCN.  All rights reserved.
##

##
# @page auditpage Audit Evaluation
#
#  This table shows the properties audited and thei results.
#
#     | No. | Property | Description | Result |
#     | --- | -------- | ----------- | ------ |
#     | xxx | Data set characteristics | xxxxxxxxxxx | xxxxxx |
#     | 1.1 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | 1.2 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | 1.3 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | xxx | Robustness | xxxxxxxxxxx | xxxxxx |
#     | 2.1 | Dataset robustness | A coefficient measure based in the distance between the train and test dataset | xxxxxx |
#     | 2.2 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | 2.3 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | xxx | Explainability | xxxxxxxxxxx | xxxxxx |
#     | 3.1 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | 3.2 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#     | 3.3 | Metrics bias | xxxxxxxxxxx | xxxxxx |
#
##

##
# @dataset Columns description
#
# 1. Anaemia: Decrease of red blood cells or hemoglobin (boolean);
# 2. Creatinine phosphokinase: Level of the CPK enzyme in the blood (mcg/L);
# 3. Diabetes:If the patient has diabetes (boolean);
# 4. Ejection fraction: Ejection fraction (EF) is a measurement, expressed as a percentage,
# of how much blood the left ventricle pumps out with each contraction;
# 5. High blood pressure: blood hypertension;
# 6. Platelets: are a component of blood whose function (along with the coagulation factors);
# 7. Serum creatinine: Serum creatinine is widely interpreted as a measure only of renal function;
# 8. Serum sodium: to see how much sodium is in your blood it is particularly important for nerve and muscle function.
#
# ![width = 300](https://miro.medium.com/max/4420/1*HDphOMQdTsRUM-O4hudIWA.png)
##

##
# @file result_py.py
#
# @brief Example Python program with Doxygen style comments.
#
# @section description_doxygen_example Description
# Example Python program with Doxygen style comments.
#
# @section libraries_main Libraries/Modules
# @import pandas as pd
# @import numpy as np
#
# @section notes_doxygen_example Notes
# - Comments are Doxygen compatible.
#
# @section author_doxygen_example Author(s)
# - Created by [Your Name] on [Date].
# - Modified by [Your Name] on [Date].
#
# @section license_doxygen_example License
# Copyright (c) 2023 UTCN.  All rights reserved.
##

import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import plotly.graph_objects as go
import plotly.express as px

SPECIAL_VAR=1

sns.set(context='notebook', style='darkgrid', palette='colorblind', font='sans-serif', font_scale=1, rc=None)

matplotlib.rcParams['figure.figsize'] =[8,8]
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams['font.family'] = 'sans-serif'

## Load the heart failure clinical records dataset
train= pd.read_csv('../heart_failure_clinical_records_dataset.csv')

# Display the first 6 rows of the dataset
train.head(6)

# Display information about the dataset, such as the number of rows, columns, and data types
train.info()

train.dtypes.value_counts().plot.pie(explode=[0.1,0.1],autopct='%1.1f%%',shadow=True)
plt.title('type of our data');

train.columns

train.describe()

train.isnull().sum()

train.hist(figsize=(15,15),edgecolor='black');

train.DEATH_EVENT.value_counts().plot.pie(explode=[0.1,0.1],autopct='%1.1f%%',shadow=True)
plt.title('the % of deaths')

plt.figure(figsize=(20,6))
sns.countplot(x='age',data=train)
plt.xticks(rotation=90)
plt.title('the ages of our persone')

fig = go.Figure()
fig.add_trace(go.Histogram(
    x = train['age'],
    xbins=dict( # bins used for histogram
        start=40,
        end=95,
        size=2
    ),
    marker_color='#e8ab60',
    opacity=1
))

fig.update_layout(
    title_text='Distribution of Age',
    xaxis_title_text='AGE',
    yaxis_title_text='COUNT', 
    bargap=0.05, # gap between bars of adjacent location coordinates
    xaxis =  {'showgrid': False },
    yaxis = {'showgrid': False },
    template = 'presentation'
)

fig.show()

fig = px.histogram(train, x="age", color="DEATH_EVENT", marginal="violin", hover_data=train.columns, 
                   title ="Distribution of AGE Vs DEATH_EVENT", 
                   labels={"age": "AGE"},
                   template="plotly",
                   
                   
                  )
fig.show()

train.sex.value_counts().plot.pie(explode=[0.1,0.1],autopct='%1.1f%%',shadow=True)

sns.countplot(x='sex',hue='DEATH_EVENT',data=train)
plt.legend(['yes','no'])

import plotly.graph_objects as go
from plotly.subplots import make_subplots

d1 = train[(train["DEATH_EVENT"]==0) & (train["sex"]==1)]
d2 = train[(train["DEATH_EVENT"]==1) & (train["sex"]==1)]
d3 = train[(train["DEATH_EVENT"]==0) & (train["sex"]==0)]
d4 = train[(train["DEATH_EVENT"]==1) & (train["sex"]==0)]

label1 = ["Male","Female"]
label2 = ['Male - Survived','Male - Died', "Female -  Survived", "Female - Died"]

values1 = [(len(d1)+len(d2)), (len(d3)+len(d4))]
values2 = [len(d1),len(d2),len(d3),len(d4)]

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=label1, values=values1, name="GENDER"),
              1, 1)
fig.add_trace(go.Pie(labels=label2, values=values2, name="GENDER VS DEATH_EVENT"),
              1, 2)

fig.update_traces(hole=.4, hoverinfo="label+percent")

fig.update_layout(
    title_text="GENDER DISTRIBUTION IN THE DATASET  \
                   GENDER VS DEATH_EVENT",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='GENDER', x=0.19, y=0.5, font_size=10, showarrow=False),
                 dict(text='GENDER VS DEATH_EVENT', x=0.84, y=0.5, font_size=9, showarrow=False)],
    autosize=False,width=1200, height=500, paper_bgcolor="white")

fig.show()

sns.barplot(x='sex',y='smoking',hue='DEATH_EVENT',data=train);

sns.countplot(x='sex',hue='smoking',data=train)
plt.legend(['yes','no']);

sns.countplot(x='sex',hue='diabetes',data=train)
plt.legend(['yes','no']);

train.diabetes.value_counts().plot.pie(explode=[0.1,0.1],autopct='%2.2f%%',shadow=True)

sns.countplot(x='diabetes',hue='DEATH_EVENT',data=train)
plt.legend(['yes','no']);

sns.boxplot(x = train.ejection_fraction, color = 'green')
plt.show()

train[train['ejection_fraction']>=70]

train = train[train['ejection_fraction']<70]

import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Histogram(
    x = train['ejection_fraction'],
    xbins=dict( # bins used for histogram
        start=14,
        end=80,
        size=2
    ),
    marker_color='#A7F432',
    opacity=1
))

fig.update_layout(
    title_text='EJECTION FRACTION DISTRIBUTION',
    xaxis_title_text='EJECTION FRACTION',
    yaxis_title_text='COUNT', 
    bargap=0.05, # gap between bars of adjacent location coordinates

    template = 'plotly_dark'
)

fig.show()

sns.boxplot(x=train.time, color = 'yellow')
plt.show()

sns.boxplot(x=train.serum_creatinine, color = 'red')
plt.show()

train.corr().style.background_gradient(cmap='coolwarm').set_precision(2)

plt.rcParams['figure.figsize']=15,6 
sns.set_style("darkgrid")

x = train.iloc[:, :-1]
y = train.iloc[:,-1]

from sklearn.ensemble import ExtraTreesClassifier

model = ExtraTreesClassifier()
model.fit(x,y)
print(model.feature_importances_) 
feat_importances = pd.Series(model.feature_importances_, index=x.columns)
feat_importances.nlargest(12).plot(kind='barh')
plt.show()

train=train.drop(['anaemia','creatinine_phosphokinase','diabetes','high_blood_pressure','platelets','sex','smoking','age'],axis=1)

train.corr().style.background_gradient(cmap='coolwarm').set_precision(3)

from sklearn.model_selection import train_test_split

x=train.drop('DEATH_EVENT',axis=1)
y=train.DEATH_EVENT

print(x.shape)
print(y.shape)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)

print(x_train)
print(y_test)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

model = LogisticRegression()

model.fit(x_train, y_train)
y_pred = model.predict(x_test)

mylist = []

cm = confusion_matrix(y_test, y_pred)

acc_logreg = accuracy_score(y_test, y_pred)

mylist.append(acc_logreg)
print(cm)
print(acc_logreg)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

list1 = []
for neighbors in range(3,10):
    classifier = KNeighborsClassifier(n_neighbors=neighbors, metric='minkowski')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_pred))
plt.plot(list(range(3,10)), list1)
plt.show()

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
acc_knn = accuracy_score(y_test, y_pred)
mylist.append(acc_knn)
print(cm)
print(acc_knn)

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score
list1 = []
for c in [0.5,0.6,0.7,0.8,0.9,1.0]:
    classifier = SVC(C = c, random_state=0, kernel = 'rbf')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_pred))
plt.plot([0.5,0.6,0.7,0.8,0.9,1.0], list1)
plt.show()

from sklearn.svm import SVC
classifier = SVC(C = 0.7, random_state=0, kernel = 'rbf')
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
acc_svc = accuracy_score(y_test, y_pred)
print(cm)
print(acc_svc)
mylist.append(acc_svc)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
list1 = []
for leaves in range(2,15):
    classifier = DecisionTreeClassifier(max_leaf_nodes = leaves, random_state=0, criterion='entropy')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_pred))
#print(mylist)
plt.plot(list(range(2,15)), list1)
plt.show()

classifier = DecisionTreeClassifier(max_leaf_nodes = 10, random_state=0, criterion='entropy')
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
acc_decisiontree = accuracy_score(y_test, y_pred)
print(cm)
print(acc_decisiontree)
mylist.append(acc_decisiontree)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
list1 = []
for estimators in range(10,30):
    classifier = RandomForestClassifier(n_estimators = estimators, random_state=0, criterion='entropy')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_pred))

plt.plot(list(range(10,30)), list1)
plt.show()

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 15, criterion='entropy', random_state=0)
classifier.fit(x_train,y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
acc_randomforest = accuracy_score(y_test, y_pred)
mylist.append(acc_randomforest)
print(cm)
print(acc_randomforest)

np.random.seed(0)
import tensorflow as tf

ann = tf.keras.models.Sequential()

ann.add(tf.keras.layers.Dense(units = 7, activation = 'relu'))

ann.add(tf.keras.layers.Dense(units = 7, activation = 'relu'))

ann.add(tf.keras.layers.Dense(units = 7, activation = 'relu'))

ann.add(tf.keras.layers.Dense(units = 7, activation = 'relu'))

ann.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy' , metrics = ['accuracy'] )

ann.fit(x_train, y_train, batch_size = 16, epochs = 100)

y_pred = ann.predict(x_test)
y_pred = (y_pred > 0.5)
np.set_printoptions()

from sklearn.metrics import confusion_matrix, accuracy_score

cm = confusion_matrix(y_test,y_pred)
print("Confusion Matrix")
print(cm)
print()

ac_ann = accuracy_score(y_test,y_pred)
print("Accuracy")
print(ac_ann)
mylist.append(ac_ann)

from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
list1 = []
for estimators in range(10,30,1):
    classifier = XGBClassifier(n_estimators = estimators, max_depth=12, subsample=0.7)
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    list1.append(accuracy_score(y_test,y_pred))

plt.plot(list(range(10,30,1)), list1)
plt.show()

from xgboost import XGBClassifier
classifier = XGBClassifier(n_estimators = 10, max_depth=12, subsample=0.7)
classifier.fit(x_train,y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
ac_xgboost = accuracy_score(y_test, y_pred)
mylist.append(ac_xgboost)
print(cm)
print(ac_xgboost)

from catboost import CatBoostClassifier
classifier = CatBoostClassifier()
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
ac_catboost = accuracy_score(y_test, y_pred)
mylist.append(ac_catboost)
print(cm)
print(ac_catboost)

models = pd.DataFrame({
    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
              'Random Forest', 'ANN',   
              'Decision Tree','xgboost','catboost'],
    'Score': [acc_svc, acc_knn, acc_logreg, 
              acc_randomforest, ac_ann, acc_decisiontree,ac_xgboost,ac_catboost
              ]})
models.sort_values(by='Score', ascending=False)

plt.rcParams['figure.figsize']=15,6 
sns.set_style("darkgrid")
ax = sns.barplot(x=models.Model, y=models.Score, palette = "rocket", saturation =1.5)
plt.xlabel("Classifier Models", fontsize = 20 )
plt.ylabel("% of Accuracy", fontsize = 20)
plt.title("Accuracy of different Classifier Models", fontsize = 20)
plt.xticks(fontsize = 12, horizontalalignment = 'center', rotation = 8)
plt.yticks(fontsize = 13)
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height:.2%}', (x + width/2, y + height*1.02), ha='center', fontsize = 'x-large')
plt.show()
