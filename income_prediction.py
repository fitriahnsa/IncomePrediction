# -*- coding: utf-8 -*-
"""Income Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FxuZ0idfWjT7ZCd0mPeQaQ68xNDeA0V2
"""

import pandas as pd

df = pd.read_csv('/adult.csv')

from google.colab import drive
drive.mount('/content/drive')

df

"""**Exploration Data**"""

df.education.value_counts()
#di sort tidak berdasarkan degree education tapi berdasarkan frekuensi data

df.workclass.value_counts()

df.occupation.value_counts()

df = pd.concat([df.drop('occupation', axis=1), pd.get_dummies(df.occupation).add_prefix('occupation_')], axis = 1)
df = pd.concat([df.drop('workclass', axis=1), pd.get_dummies(df.workclass).add_prefix('workclass_')], axis = 1)
df = df.drop('education', axis =1)
df = pd.concat([df.drop('marital-status', axis=1), pd.get_dummies(df['marital-status']).add_prefix('marital-status_')], axis = 1)
df = pd.concat([df.drop('relationship', axis=1), pd.get_dummies(df.relationship).add_prefix('relationship_')], axis = 1)
df = pd.concat([df.drop('race', axis=1), pd.get_dummies(df.race).add_prefix('race_')], axis = 1)
df = pd.concat([df.drop('native-country', axis=1), pd.get_dummies(df['native-country']).add_prefix('native-country')], axis = 1)

df

df['gender'] = df['gender'].apply(lambda x: 1 if x == 'Male' else 0)
df['income'] = df['income'].apply(lambda x: 1 if x == '>50K' else 0)

df.columns.values

df

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(18,12))
sns.heatmap(df.corr(), annot = False, cmap ='coolwarm')

df.corr()

correlations = df.corr()['income'].abs()
sorted_correlations = correlations.sort_values()
num_cols_to_drop = int(0.8 * len (df.columns))
cols_to_drop = sorted_correlations.iloc [:num_cols_to_drop].index
df_dropped = df.drop(cols_to_drop, axis = 1)

df_dropped

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(15,10))
sns.heatmap(df_dropped.corr(), annot = True, cmap ='coolwarm')
plt.show()

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = df.drop('fnlwgt', axis=1)

train_df, test_df = train_test_split(df, test_size = 0.2)
train_df

test_df

train_X = train_df.drop('income', axis=1)
train_Y = train_df['income']

test_X = test_df.drop('income', axis=1)
test_Y = test_df['income']

forest = RandomForestClassifier(
)
forest.fit(train_X, train_Y)

forest.score(test_X, test_Y)

forest.feature_importances_

importances = dict(zip(forest.feature_names_in_, forest.feature_importances_))
importances = {k: v for k, v in sorted(importances.items(), key = lambda x: x[1], reverse = True)}

importances

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators' : [50, 100,250],
    'max_depth' : [5,10,30,None],
    'min_samples_split' : [2,4],
    'max_features' : ['sqrt', 'log2']
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(),
                           param_grid=param_grid, verbose=10)

grid_search = GridSearchCV(estimator=RandomForestClassifier(),
                          param_grid=param_grid, verbose=10 )

grid_search.fit(train_X, train_Y)

grid_search.best_estimator_

forest = grid_search.best_estimator_

forest.score(test_X, test_Y)

importances = dict(zip(forest.feature_names_in_, forest.feature_importances_))
importances = {k: v for k, v in sorted(importances.items(), key = lambda x: x[1], reverse = True)}

importances