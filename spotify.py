client_id = '7732e980bc9a4abda4e0341a5aa0adce'
client_secret = '28022c734b5145ea9b15e55bfe5cc312'
username = 'abinam913'

import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = sp.Spotify(client_credentials_manager=client_credentials_manager)

# Store playlists
playlists = sp.user_playlists(username)

# Explore playlists
playlists.keys()
playlists.values()

playlists['href']
playlists['items']
playlists['limit']
playlists['next']

# Declare empty lists for storage
uri_list = list()
id_list = list()

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
        uri_list.append(playlist['uri'])
        id_list.append(playlist['id'])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

# Get playlist tracks
playlist_id = id_list[0]
tracks = sp.user_playlist_tracks(username, playlist_id)


#create list from playlist tracks
track_list = []

def create_track_list(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_list.append(" %d| %s| %s| %s| %d| %d" % (i, track['artists'][0]['name'], track['name'], track['album']['name'],
                                                       track['duration_ms'], track['popularity']))

create_track_list(tracks)

#create dataframe from list
import pandas as pd
newList = []
for i in track_list:
    newList.append(i.split('|'))
df_ = pd.DataFrame(newList)


df_.columns = ['Track_number', 'Artist', 'Song', 'Album', 'Duration_ms', 'Popularity']

#df_.to_csv('Metal.csv')

metalData = df_
df_['Duration_ms'] = df_['Duration_ms'].astype(int)
df_['Popularity'] = df_['Popularity'].astype(int)

import matplotlib.pyplot as plt
import numpy as np

plt.scatter(df_.Duration_ms, df_.Popularity)
plt.xticks(rotation=45)
plt.locator_params(axis='y', nticks=10)
plt.locator_params(axis='x', nticks=10)
plt.xlabel('Duration (ms)')
plt.ylabel('Popularity')
plt.title('Relationship Between Popularity and Song Length')
plt.show()

plt.hist(df_.Duration_ms)
plt.xlabel('Duration (ms)')
plt.title('Duration in Miliseconds Histogram')
plt.show()

print(df_.describe())

### Build a linear model
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd


# Define the data/predictors as the pre-set feature names
X = pd.DataFrame(df_.Duration_ms, columns=['Duration_ms'])

# Put the target in another data frame
Y = pd.DataFrame(df_.Popularity, columns=["Popularity"])

# Create linear regression object
lm = linear_model.LinearRegression()

# Train the model and predict
lm.fit(X, Y)
preds = lm.predict(X)
preds

#R^2
print(lm.score(X,Y))

# Coefficients
print('The slope coefficient for song duration is', lm.coef_)

# Intercept
lm.intercept_

print('The slope coefficient for song duration is', lm.coef_)

# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(Y, preds))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.6f' % r2_score(Y, preds))



# The other way to do linear regression in Python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Build reg model
model_fit = smf.ols('Popularity ~ Duration_ms', data=df_).fit()


# Other regresion attributes
# fitted values (need a constant term for intercept)
model_fitted_y = model_fit.fittedvalues

# model residuals
model_residuals = model_fit.resid

# calculate sum of squared errors
np.sum(model_residuals**2)


import seaborn as sns
plot_lm_1 = plt.figure(1)
plot_lm_1.set_figheight(8)
plot_lm_1.set_figwidth(12)
plot_lm_1.axes[0] = sns.residplot(model_fitted_y, 'Popularity', data=df_, 
                          lowess=True, 
                          scatter_kws={'alpha': 0.5}, 
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})
plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')