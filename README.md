# Black-Litterman-Implied-Covariance

This project focuses on constructing the covariance matrix of stock returns for nearly 10,000 stocks. This project does two things:
- Speeds up the Black Litterman process by allowing for less computationally expensive inversion of the covariance matrix, which is required for the model
- Allows for additional detailed analysis of stocks and industries (discussed below)

## Project Overview

### Part 1: Index Construction
Historical stock data (6 billion rows of vertically stacked data over a 3-year time frame) from WRDS is processed into usable formats. The data is cleaned and organized into dictionaries for each ticker. The following key dataframes are created:
- Returns DataFrame
- Cumulative Returns DataFrame
- Market Cap DataFrame
- Weights DataFrame (market-cap weighted)
- Index DataFrame (market-cap weighted average of returns)
- Cumulative Index DataFrame

Stocks are also subdivided into industries using SIC and Permno code mappings. Monte Carlo simulations based on geometric Brownian motion are used to predict future growth paths for each industry using the constructed indices, which are plotted alongside the individual cumulative stock returns.

### Part 2: Factor Regression, Matrix Construction, and Visualization
This part constructs the implied covariance matrix, using factor regression modelling among other components. Full description of the process is shown in the Jupyter Notebook. 

This section also includes visualizations of the resulting covariance matrices. 
**Note:** The visualizations of covariance matrices have been expanded into a separate project, which is currently being developed into a website. You can check out the separate project here: [Placeholder for project link].

## Files

### Main Notebooks
- **"Clean File Part 1 (Index and Factor Construction).ipynb"**  
   Contains data cleaning, index construction, Monte Carlo simulations, and plotting of predicted industry growth.

- **"Clean File Part 2 (Matrix Construction).ipynb"**  
   Focuses on the regression model and implied covariance matrix construction for the Black-Litterman model.

### Supporting Files
- **SIC_to_industry.csv**  
   Contains mappings from SIC codes to industries. See code for mapping.

- **permno_sic.csv**  
   Provides mappings between SIC codes and Permno codes. See code for mapping. 

- **timer_class.py**  
   Creates a Timer() object that can be used to time any of the processes. Take note of time taken per cell if choosing to re-run the notebook yourself. 

Other supporting files used throughout the project can be viewed in the Jupyter notebooks for further reference. See commenting for any relevant section. 

## Installation and Usage

1. Clone or download the repository.
2. Place all files in the same directory.
3. Check the Jupyter notebooks for the required libraries and imports. 
4. Run the Jupyter notebooks in order to process the data, perform regression modeling, and visualize the results.

Downloading the files alone should display all the results.

## Features
- Index construction and plotting for nearly 10,000 stocks and their industries.
- Monte Carlo simulations to predict the growth of industry indices.
- Matrix construction for Black-Litterman model using factor regression.
- Visualizations of covariance matrices (expanded into a separate project).

## Data Source
Data for this project is sourced from WRDS, a database for financial and economic data.
