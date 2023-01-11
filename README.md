# ML-Spotify-Trends
Using machine learning to explore trends in the billboard top 100 charts with Spotify's dataset

# DATA

Song lists were pulled from Billboard’s top year-end charts, broken down by genre and chart year. The following 
genre/year breakdowns were used:
- Pop – Top 50 from 2008-2020
- Country – Top 100 from 2002-2020
- R&B – Top 100 from 2002-2020
- Jazz – Top 50 from 2006-2020
- Latin – Top 100 from 2006-2020

In addition to these ‘popular’ songs, a random list of unpopular songs was pulled with release dates in the same chart 
years, from the same genres.
All track data was pulled from Spotify’s dataset, except for year and chart rank, which are Billboard values.


# GOALS
- Produce, clean, and analyze song data from Spotify using Billboard charts
- Classify songs as ‘popular’ vs ‘unpopular’
- Cluster songs by genre
- Predict ‘popular’ song chart rank on top 100 charts


# METHODS
Song data was extracted using a scraping script to pull the top charts from Billboard’s website. After the song titles were 
retrieved, Spotify’s API was used to search for the song titles and artists to pull the relevant data down. After review and 
cleanup these songs were merged with a randomly pulled list of songs in the same genre/chart year as the popular 
songs. A ratio of about 1/4 was used for popular/unpopular track numbers.
Classification methods evaluated were Decision Trees, Naïve Bayes, and K Nearest Neighbors, with accuracy measured 
using precision, recall, and f1-score metrics. Classes used were popular and unpopular, and separately the 5 genres. 
Evaluation was done using a grid search to identify optimal parameters and performed on subsets of the data breaking 
by genre, all data combined, and data after performing Principal Component Analysis.
Clustering methods evaluated were DBSCAN and kMeans, with accuracy measured using homogeneity and 
completeness scores. Clusters were intended to be based on the 5 genres. Evaluation was done using various epsilon 
values and minimum sample counts for DBSCAN, and 5 clusters for kMeans. Again, data used was broken by genre, as 
well as all data combined, and data after PCA was performed.
Prediction methods evaluated were Ridge, Lasso, and Stochastic Gradient Descent linear regression models, with 
accuracy measured in root mean squared error and goodness of fit, R^2. Models were intended to predict popular songs 
chart ranking on their respective chart. Evaluation was done using a grid search to identify optimal parameters and was 
performed on a breakdown of genres and combined data, with several variants, including PCA and a subset of only the 3 
most recent years of data.


# RESULTS
Classification of popular vs. unpopular songs, and of genres, clustering by genre, and prediction of chart rank based on 
popular songs, all revealed no trends in the data strong enough to reliably perform any task well.
It can be safely stated at this point that popular songs, within the context of the Spotify dataset, have no discernable 
difference from unpopular songs, and that a popular song’s position on the Billboard’s top charts cannot be assumed 
based on its relation to other popular songs.
It seems overall that the song data is relatively random, which while not a hard statement to accept, (it’s easy to accept 
that popular songs are popular randomly), is a bit disappointing regarding this project.
