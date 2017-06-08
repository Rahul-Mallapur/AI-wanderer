import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import tweepy
from textblob import TextBlob
from keras.models import Sequential
from keras.layers import Dense


consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#would use it later
def stock_sentiment(stock, num_tweets):
    public_tweets = api.search(stock)
    positive, null = 0,0
    
    for tweet in public_tweets:
        analysis = TextBlob(tweet.text).sentiment
        if analysis.subjectivity == 0:
            null += 1
        if analysis.polarity > 0:
            positive += 1
        
        if positive > (num_tweets-null)/2:
            return True
            
                                     
    
dates = []
prices = []

def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            dates.append(int(row[0]))
            prices.append(float(row[1]))
    return    

def predict_prices(dates, prices, x):
    dates = np.reshape(dates,(len(dates),1))
    
    svr_lin = SVR(kernel = 'linear', C=1e3)
    svr_poly = SVR(kernel = 'poly', C=1e3, degree = 2)
    svr_rbf = SVR(kernel = 'rbf', C=1e3, gamma = 0.1)
    
    svr_lin.fit(dates,prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)
    
    plt.scatter(dates, prices, color='black', label = 'Data')
    plt.plot(dates, svr_lin.predict(dates), color='red', label='Linear model')
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    plt.plot(dates, svr_rbf.predict(dates), color='green', label='RBF model')
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()
    
    return svr_lin.predict(x)[0], svr_poly.predict(x)[0], svr_rbf.predict(x)[0]

stock = 'Airtel'
get_data('stockdata_airtel.csv')
predicted_price = predict_prices(dates, prices, 70)    
                
    
                                   