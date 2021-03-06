# -*- coding: utf-8 -*-
"""Homework2_SharpeRatio

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IlDxIVszSvOA9-eZYhGeOg_cP-SimdgT

Homework 2 "Algorithmic trading" course.

Building portfolio.

Student name: Madina Kudaibergenova

---

Method to determine weights: Sharpe ratio

Data source: Yahoo finance

Monte Carlo simulations to assign random weights to the stocks and calculate volatility

Start date is 4th of January 2021, end date is 12th of April 2021

Only close price was used
"""

# importing necessary libraries
import ssl # TLS/SSL wrapper for socket objects
from functools import wraps 
import numpy as np # perform math calculations
import pandas as pd # data analysis
import pandas_datareader.data as web # collect data from resources 
import matplotlib.pyplot as plt # draw graphics

# this code is based on https://github.com/mekriti/Portfolio-diversification-using-Sharpe-Ratio

# setting up connection
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)

# list of stocks in portfolio
stocks = ['BHP', 'DE', 'FE', 'GOOG','GS','JNJ', 'KO', 'T', 'WMT', 'XOM']

# download daily price data for each of the stocks in the portfolio
data = web.DataReader(stocks,data_source='yahoo',start='01/04/2021', end='04/12/2021')['Close']
 
# convert daily stock prices into daily returns
returns = data.pct_change()

# printing data (I have compared it to the given, and they are equal)
data

# calculate mean daily return and covariance of daily returns
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()

# set number of runs of random portfolio weights
num_portfolios = 10000
 
# set up array to hold results
# Array to hold weight for each stock
results = np.zeros((3+len(stocks),num_portfolios))

for i in range(num_portfolios):
    # select random weights for portfolio holdings
    weights = np.array(np.random.random(10))
    # normalizing weights
    weights /= np.sum(weights)
 
    # calculate portfolio return and volatility(which is a standard deviation)
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights)))*np.sqrt(252)
 
    # store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    # store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = ( results[0,i] )/ (results[1,i] )
    # iterate through the weight vector and add data to results array
    for j in range(0,10):
        results[j+3,i] = weights[j]

results_frame = pd.DataFrame(results.T, columns=['ret','stdev','sharpe',stocks[0], stocks[1], 
                                                 stocks[2], stocks[3], stocks[4], stocks[5], 
                                                 stocks[6], stocks[7], stocks[8], stocks[9]])
# locate position of portfolio with highest Sharpe Ratio
maxsp = results_frame.iloc[results_frame[['sharpe']].idxmax()]
# locate positon of portfolio with minimum standard deviation
minvp = results_frame.iloc[results_frame['stdev'].idxmin()]
print(results_frame)
# create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.ret,c = results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()

maxsp_array = pd.DataFrame.to_numpy(maxsp) # converting DataFrame to numpy for convenience

# print the line that was chosen as a max Sharpe Ratio
maxsp

# weights for each company in portfolio
print("BHP: ", np.round(maxsp_array[0][3],6)," / DE: ", np.round(maxsp_array[0][4],6), 
      " / FE: ", np.round(maxsp_array[0][5],6), " / GOOG: ", np.round(maxsp_array[0][6],6),'\n'
      "GS: ", np.round(maxsp_array[0][7],6), " / JNJ: ", np.round(maxsp_array[0][8],6),
      " / KO: ", np.round(maxsp_array[0][9],6), " / T: ", np.round(maxsp_array[0][10],6),'\n'
      "WMT: ", np.round(maxsp_array[0][11],6), " / XOM: ", np.round(maxsp_array[0][12],6))

print("Expected portfolio return: ", np.round(100*maxsp_array[0][0],2), "%")
print("Expected portfolio volatility: ", np.round(100*np.average(minvp),2), "%")
print("Maximum Sharpe ration of the portfolio: ", np.round(np.max(results[2]),2))