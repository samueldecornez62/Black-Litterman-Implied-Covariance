#!/usr/bin/env python
# coding: utf-8

# In[9]:


### ONLY FIRST 4  DATAFRAMES: returns, cumulative returns, market cap, weights 

import pandas as pd
import numpy as np
import warnings

import sys
import os 

#Completely optional, this helps time different parts of the code
from timer_class import Timer

timer = Timer()


#Input parameters:
#List of tickers we want to collect data for; tickers are sorted by industry into some lists 
#Entire dataframe returns_df is input as well, same for entire market_cap_df
def process_industry_subset(subset_list, returns_df, market_cap_df):

    #Open the context manager to ignore performance warning (concatenation leads to errors)
    with warnings.catch_warnings():
        #Specify which error (PerformanceWarning and SettingWithCopyWarning) to ignore 
        warnings.simplefilter('ignore', category=pd.errors.PerformanceWarning)
        warnings.simplefilter('ignore', category=pd.errors.SettingWithCopyWarning)

    
        # Step 1: Extract the returns_df with only these tickers
        subset_returns_df = returns_df[subset_list]
        
        print('Step 1 done: Returns dataframe.')
        
        # Step 2: Calculate cumulative returns
        cum_returns_list = []
        
        timer.start()
        
        for ticker in subset_returns_df.columns:
            cum_returns = pd.Series(index=subset_returns_df.index, dtype='float64')
            started = False
            for i in range(len(subset_returns_df)):
                if pd.notna(subset_returns_df[ticker].iloc[i]):
                    if not started:
                        cum_returns.iloc[i] = 1 + subset_returns_df[ticker].iloc[i]
                        started = True
                    else:
                        cum_returns.iloc[i] = cum_returns.iloc[i-1] * (1 + subset_returns_df[ticker].iloc[i])
                else:
                    if started:
                        cum_returns.iloc[i] = cum_returns.iloc[i-1]
            
            cum_returns.name = ticker
            cum_returns_list.append(cum_returns)
        
        subset_cum_stock_returns_df = pd.concat(cum_returns_list, axis=1)
        
        print('Step 2 done: Cumulative Returns dataframe.')
        
        timer.end()  # Assuming this is for timing, replace with actual timing code if necessary
        
        # Step 3: Extract relevant market_cap_df data
        subset_market_cap_df = market_cap_df[subset_list]
        subset_market_cap_df['Total Market Cap'] = subset_market_cap_df.sum(axis=1)
        
        print('Step 3 done: Market cap dataframe.')
        
        # Step 4: Get weights with the new subset
        timer.start()  # Assuming this is for timing, replace with actual timing code if necessary
        
        subset_weights_df = subset_market_cap_df.copy()
        subset_weights_df = subset_weights_df.divide(subset_weights_df['Total Market Cap'], axis=0)
        subset_weights_df.rename(columns={'Total Market Cap': 'Total Weight'}, inplace=True)
        
        print('Step 4 done: Weights dataframe.')
        print('\n----- Returning values -----')
        
        
        timer.end()  # Assuming this is for timing, replace with actual timing code if necessary

        
        return (subset_returns_df, subset_cum_stock_returns_df, subset_market_cap_df, 
            subset_weights_df)
    



# In[11]:


#NESXT 2:



#Inputs into this second function are returned from the one directly above 
def compute_indices(subset_returns_df, subset_weights_df, subset_cum_stock_returns_df):
    # Drop the 'Total Weight' column and fill NaNs with 0
    new_weights_df = subset_weights_df.drop(columns='Total Weight').fillna(0)
    subset_returns_df = subset_returns_df.fillna(0)

    # Transpose the weights DataFrame
    transposed_weights_df = new_weights_df.T
    transposed_weights_df.index = subset_returns_df.columns

    # Compute matrix multiplication
    result_df = subset_returns_df.dot(transposed_weights_df)

    # Initialize index_df with NaNs
    index_df = pd.DataFrame(index=subset_returns_df.index, columns=['Diagonal'])

    if result_df.shape[0] == result_df.shape[1]:
        # Extract diagonal elements and assign to index_df
        diagonal_elements = np.diag(result_df)
        index_df['Diagonal'] = diagonal_elements

    # Initialize cumulative_index_df
    cum_index_df = pd.DataFrame(index=subset_cum_stock_returns_df.index, columns=['Cumulative'])

    # Set the first row of cumulative_index_df
    cum_index_df.iloc[0] = 1 + index_df['Diagonal'].iloc[0]

    # Populate the rest of cumulative_index_df
    for i in range(1, len(cum_index_df)):
        cum_index_df.iloc[i] = cum_index_df.iloc[i - 1] * (1 + index_df['Diagonal'].iloc[i])

    # Return both DataFrames
    return (index_df, cum_index_df)


# In[ ]:




