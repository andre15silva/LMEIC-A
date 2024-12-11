import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error

XX = pd.read_csv("./KV periodic - JNSM 2017/X.csv",
        converters={'TimeStamp': pd.Timestamp})
YY = pd.read_csv("./KV periodic - JNSM 2017/Y.csv",
        converters={'TimeStamp': pd.Timestamp})

#XX = XX.iloc[:1000,:]
#YY = YY.iloc[:1000,:]

# Convert timestamps to timedeltas
XX.iloc[:,0] = (XX.iloc[:,0] - XX.iloc[0,0]) // pd.Timedelta('1s')
YY.iloc[:,0] = (YY.iloc[:,0] - YY.iloc[0,0]) // pd.Timedelta('1s')

# Pre-process
XX.iloc[:,1:] = scale(XX.iloc[:,1:], axis=0)

# Remove outliers
T = 40
XX = XX[~XX.iloc[:,1:].gt(T).any(1)]
XX = XX[~XX.iloc[:,1:].lt(-T).any(1)]
YY = YY.loc[XX.index]

y = YY['ReadsAvg']

# Split training and testing
T = int(0.7 * y.shape[0])
y = y.tolist()

# ARIMA
h = 10
nmaes = pd.DataFrame([[0 for i in range(1,11)] for j in range(0,11)], columns=[i for i in range(1,11)])
for p in range(1,11):
    print("ARIMA MODEL " + str(p))
    # Train model
    model = ARIMA(y, order=(p,0,p)).fit()

    observations = []
    predictions = []

    # Generate pairs to test
    for i in range(T+p, len(y)-h-1):
        observations += [[y[j] for j in range(i, i+h+1)]]
        predict = model.predict(start=i,end=i+h,dynamic=True,typ="levels")
        predictions += [predict.tolist()]

    observations = pd.DataFrame(observations)
    predictions = pd.DataFrame(predictions)

    # Calculate NMAES
    for j in range(h+1):
        nmaes.iloc[j,p-1] = mean_absolute_error(observations.iloc[:,j], predictions.iloc[:,j]) / np.mean(observations.iloc[:,j])
        
fig, ax = plt.subplots(figsize=(10,9))
sns.heatmap(nmaes, annot=True, fmt=".4f", ax=ax)
ax.set_xlabel("lag")
ax.set_ylabel("h")
plt.savefig("arima_d_0_nmae_heatmap.png")
plt.clf()

# ARIMA
h = 10
nmaes = pd.DataFrame([[0 for i in range(1,11)] for j in range(0,11)], columns=[i for i in range(1,11)])
for p in range(1,11):
    print("ARIMA MODEL " + str(p))
    # Train model
    model = ARIMA(y, order=(p,1,p)).fit()

    observations = []
    predictions = []

    # Generate pairs to test
    for i in range(T+p, len(y)-h-1):
        observations += [[y[j] for j in range(i, i+h+1)]]
        predict = model.predict(start=i,end=i+h,dynamic=True,typ="levels")
        predictions += [predict.tolist()]

    observations = pd.DataFrame(observations)
    predictions = pd.DataFrame(predictions)

    # Calculate NMAES
    for j in range(h+1):
        nmaes.iloc[j,p-1] = mean_absolute_error(observations.iloc[:,j], predictions.iloc[:,j]) / np.mean(observations.iloc[:,j])
        
fig, ax = plt.subplots(figsize=(10,9))
sns.heatmap(nmaes, annot=True, fmt=".4f", ax=ax)
ax.set_xlabel("lag")
ax.set_ylabel("h")
plt.savefig("arima_d_1_nmae_heatmap.png")
plt.clf()