#!/usr/bin/env python
# coding: utf-8

# ### This was converted to a .py for modular importing

# In[5]:


'''
This file contains some code to plot 2 graphs. This function is created to avoid clutter in main file for plotting by industry.
The first plot runs a Monte Carlo simulation using the Geometric Brownian Motion equation. 
This function first calculates mu and sigma, then runs the simulation.
Output is a plot of historical data continued by expected path of index, and a plot of index performance relative to individual stocks. 
The idea is to change this to a Kalman filter style prediction model, to further improve the accuracy of future index prediction. 
Coming soon.
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[9]:


#Right now just plot for a year, go and adust time and timestep parameters to change in future
def plotting_graphs(current_cum_index_df, current_cum_stock_returns_df, num_simulations = 1000):
    #Ensure the 'Cumulative' column is numeric
    current_cum_index_df['Cumulative'] = pd.to_numeric(current_cum_index_df['Cumulative'], errors='coerce')

    #Daily log returns from the cumulative index
    current_cum_index_df['log return'] = np.log(current_cum_index_df['Cumulative'])

    #Dirft is the average of these log returns
    mu = current_cum_index_df['log return'].mean()
    #Volatility is the standard deviation of the log returns
    sigma = current_cum_index_df['log return'].std()


    #Last observed price is the last value of known values in cutoff_index_df 
    S0 = current_cum_index_df['Cumulative'].iloc[-1]
    last_date = current_cum_index_df.index[-1]
    T = 1.0 # Time period for prediction in years
    dt = 1/252 # Daily time step
    N = int(T / dt) # Number of time steps

    #Store each simulation; dimensions are num_simulations by N, number of predicted values in our year 
    simulations = np.zeros((num_simulations, N))

    #Start simulating 
    for i in range(num_simulations):
        #Initialize array to store vals 
        S = np.zeros(N+1)
        #First value always same for aech simulation, last observed point 
        S[0] = S0
        #Time stepping up now 
        for t in range(1, N+1):
            #Generate a new random component in brownian differential 
            Z = np.random.normal(0,1)
            #Store current time t value 
            S[t]  = S[t-1] * np.exp((mu - 0.5 * sigma**2) * dt     +     sigma * np.sqrt(dt) * Z)
        #After loading all N values for this simulation i, store all results 
        simulations[i, :] = S[1:]
        
        
    #Collect simulation average 
    average_simulation = simulations.mean(axis=0)

    #Dates for predicted values; 
        #Start date is last date of our data + 1 day
        #N periods 
        #B is business days for weekdays 
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=N, freq='B')


    # Put side by side, i.e. 1 row, 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    ## First block of code; plot both historical data and predictions

    #Plot historical data
    ax1.plot(current_cum_index_df.index, current_cum_index_df['Cumulative'], 'k-', linewidth=2, label='Historical Data')
    #Plot individual simulations with lower opacity
    for i in range(num_simulations):
        ax1.plot(future_dates, simulations[i,:], 'b-', alpha=0.1)
    #Plot average of simulations 
    ax1.plot(future_dates, average_simulation, 'r-', linewidth=2, label='Average Expected Path')
    
    #Set labels, title, and grid for the first plot
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Value')
    ax1.set_title('Past Data and GBM MCMC Prediction for Index')
    ax1.legend()
    ax1.grid(True)
   
    ## Second block of code 
    y_min = current_cum_index_df['Cumulative'].min()
    y_max = current_cum_index_df['Cumulative'].max()
    # Add some padding (10% above and below)
    padding = 0.1 * (y_max - y_min)
    #Add extra padding above
    ax2.set_ylim(y_min - padding, y_max + 2*padding)
    
    # Plot cumulative returns for individual stocks
    for column in current_cum_stock_returns_df.columns:
        ax2.plot(current_cum_stock_returns_df.index, current_cum_stock_returns_df[column], label=column)
    
    # Plot the cumulative returns of the index with a thicker black line
    ax2.plot(current_cum_index_df.index, current_cum_index_df['Cumulative'], linestyle='-', linewidth=5, color='black', label='Index')
    
    # Set labels, title, and grid for the second plot
    ax2.set_title('Cumulative Returns of Stocks and Index')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cumulative Return')
    ax2.grid(True)
    
    # Display both plots side by side
    plt.tight_layout()
    plt.show()


# In[ ]:




