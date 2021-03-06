# -*- coding: utf-8 -*-
"""Thesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15EI5Ei7i1QdFXLv3zy959CmUZtxJc1xk
"""

# Commented out IPython magic to ensure Python compatibility.
#loading libraries
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import statsmodels.api as sm
import patsy
import scipy.stats as stats
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, ElasticNet, ElasticNetCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

#code retreived from: https://github.com/ajeya-bhat/Data-Analytics/blob/master/code/Neural_Network.py
#These functions automatically preprocess the data, preparing it for the model training 

def combined_position(x):
    #Combining the similar Position Players under a single name for simplicity
    if x in ['ST','LW','RW','CF','RF','LF','RS','LS']: #All the forward positions.
        return 'Forward'
    elif x in ['CM','LM','LDM','RM','CDM','CAM','RDM','LAM','RAM','LCM','RCM']: #All midfield positions.
        return 'Midfielder'
    elif x in ['LCB','RCB','LWB','RWB','LB','CB','RB']: # All defending positions
        return 'Defender'
    elif x in ['GK']: #All goalkeepers
        return 'GoalKeeper'
    
def preprocessing(data):

    
    removing_list = list(range(56,70))+list(range(77,106)) #list unwanted features from the data
    data.drop(data.columns[removing_list], axis = 1, inplace = True) #Removing the unwanted features.
    data.drop(['sofifa_id','short_name','nationality','player_url','dob','real_face','player_traits',
                'long_name','club_name','league_name','player_tags','body_type','wage_eur','team_jersey_number',
                'loaned_from','joined','contract_valid_until','nation_position','nation_jersey_number',
                'attacking_heading_accuracy','attacking_short_passing','work_rate','attacking_volleys','skill_fk_accuracy'
                ,'skill_curve','weak_foot','team_position', 'release_clause_eur'],inplace = True,axis = 1) 
    data[data['value_eur'] >= 0]
    data['player_positions'] = data['player_positions'].map(lambda x: x.split(',')[0] if ',' in x else x)
    data['player_positions'] = data['player_positions'].map(combined_position)
    data.fillna(0)

    data = pd.get_dummies(data, columns=['player_positions','preferred_foot'])
    return data

data_21 = pd.read_csv('players_21.csv')
df = data_21
df1 = preprocessing(df)
X = df1.drop('value_eur',axis = 1)
y = df1.value_eur
X = pd.DataFrame(df2).fillna(0)

#code retreived from: https://github.com/tanpengshi/Metis_Project_2_FIFA_Players/blob/master/Scripts%20and%20Data/Regression_Fifa_Market_Final_v2.ipynb
corr_matrix = data_21.corr()
corr_matrix

#code retreived from: https://github.com/tanpengshi/Metis_Project_2_FIFA_Players/blob/master/Scripts%20and%20Data/Regression_Fifa_Market_Final_v2.ipynb
corr_matrix = df.corr()
fig = plt.figure(figsize=[10,8])
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix,cmap='seismic',linewidth=1,linecolor='white',vmax = 1, vmin=-1,mask=mask, annot=True,fmt='0.2f')
plt.title('Correlation Heatmap', weight='bold',fontsize=20)
plt.savefig('heatmap2.png',transparent=True, bbox_inches='tight')

y_mean , y_std = y.mean() , y.std()
Y_norm=( y - y.mean())/ y.std()
Y = Y_norm
print( y_mean )
print( y_std ) 
label_encoder = LabelEncoder()
Y = label_encoder.fit_transform( Y )

#Splitting into test and train
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)
print(X_test.shape,X_train.shape)
print(y_test.shape,y_train.shape)

#Applying Linear Regression
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
from sklearn.metrics import r2_score, mean_squared_error
print('r2 score: '+str(r2_score(y_test, predictions)))
print('RMSE : '+str(np.sqrt(mean_squared_error(y_test, predictions))))

#Code retrieved from: https://github.com/tanpengshi/Metis_Project_2_FIFA_Players/blob/master/Scripts%20and%20Data/Regression_Fifa_Market_Final_v2.ipynb
# Final model reaching best accuracy metrics
from sklearn.neural_network import MLPRegressor

clf = MLPRegressor(hidden_layer_sizes=(40,100,60), learning_rate_init=0.001, random_state=1, max_iter=1000)
licz=[]
accu=[]
loss=[]
test=[]
for i in range(1000):
    clf.fit(X_train, y_train)
    licz.append(i)
    accu.append(clf.score(X_train, y_train))
    loss.append(clf.loss_)
    test.append(clf.score(X=X_test, y=y_test))
    if i%50==0: 
        print("iter",i,"\taccuracy",clf.score(X_train, y_train),"\ttest",clf.score(X=X_test, y=y_test),"\tloss",clf.loss_)
import matplotlib.pyplot as plt
print(clf.score(X=X_test, y=y_test))
plt.plot(licz[5:],accu[5:], loss[5:])

#2 hidden layer model
clf = MLPRegressor(hidden_layer_sizes=(40,100), learning_rate_init=0.001, random_state=1, max_iter=1000, warm_start=True)
licz=[]
accu=[]
loss=[]
test=[]
for i in range(1000):
    clf.fit(X_train, y_train)
    licz.append(i)
    accu.append(clf.score(X_train, y_train))
    loss.append(clf.loss_)
    test.append(clf.score(X=X_test, y=y_test))
    if i%50==0: 
        print("iter",i,"\taccuracy",clf.score(X_train, y_train),"\ttest",clf.score(X=X_test, y=y_test),"\tloss",clf.loss_)
import matplotlib.pyplot as plt
print(clf.score(X=X_test, y=y_test))
plt.plot(licz[5:],accu[5:], loss[5:])

from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, pred, squared=False)
#str(np.sqrt(mean_squared_error(y_test, predictions)))

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, pred)

pred = clf.predict(X_test)

r2_score(y_test, pred)

#4 hidden layer model
clf = MLPRegressor(hidden_layer_sizes=(40, 100, 100, 60), learning_rate_init=0.001, random_state=1, max_iter=1000, warm_start=True)
licz=[]
accu=[]
loss=[]
test=[]
for i in range(1000):
    clf.fit(X_train, y_train)
    licz.append(i)
    accu.append(clf.score(X_train, y_train))
    loss.append(clf.loss_)
    test.append(clf.score(X=X_test, y=y_test))
    if i%50==0: 
        print("iter",i,"\taccuracy",clf.score(X_train, y_train),"\ttest",clf.score(X=X_test, y=y_test),"\tloss",clf.loss_)
import matplotlib.pyplot as plt
print(clf.score(X=X_test, y=y_test))
plt.plot(licz[5:],accu[5:], loss[5:])

def print_accuracy(f):
    print("Root mean squared test error = {0}".format(np.sqrt(np.mean((f(X_test) - y_test)**2))))
    time.sleep(0.5) # to let the print get out before any progress bars

print_accuracy(clf.predict)

!pip install shap

import shap

# Code retrieved from https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/model_agnostic/Diabetes%20regression.html
X_train_summary = shap.kmeans(X_train, 10)

# Code retrieved from https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/model_agnostic/Diabetes%20regression.html
explainer = shap.KernelExplainer(clf.predict, X_train_summary)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)

# Code retrieved from https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/model_agnostic/Diabetes%20regression.html
shap.dependence_plot("age", shap_values, X_test)

shap.summary_plot(shap_values, X_train, plot_type="bar")

shap.dependence_plot("dribbling", shap_values, X_test)

