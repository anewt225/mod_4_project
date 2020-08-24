# Real Estate Consulting Proposal
Flatiron Mod 4 Project

## Overview
This project, a consulting proposal for a real estate investment firm, uses Time Series Analysis to present the top 5 zip codes for the firm to invest in in the US. 

### ReadMe Navigation

1. [Repository Navigation](#Repository-Navigation)

2. [Business Understanding](#Business-Understanding)

3. [Data Understanding](#Data-Understanding)

4. [Predictive Analysis](#Predictive-Analysis)
    1. Model Performance
    2. Prediction

5. [Conclusion](#Conclusion)
    1. Recommendations
    2. Areas for Growth

8. [Project Info](#Project-Info)

***

## Repository Navigation
- [DATA:](data)
    - [Raw Folder](data/raw)
        - [Original Dataset](data/raw/zillow_data.csv)
    - [Processed Folder](data/processed)
        - [Original Dataset Organized by Zip Codes](data/processed/zipcodes.pkl)
        - [Modified Zip Codes for EDA](data/wip/zip_df.pkl)
        - [First Attempt Median Predictions](data/processed/low_median_previous_df.pkl)
        - [Low Median Test Set](data/processed/low_median_test_df.pkl)
        - [Low Median Train Set](data/processed/low_median_train_df.pkl)
        - [Low Median Predictions](data/processed/low_medians_predictions_df.pkl)
        - [Predictions for High Median Range](data/processed/high_medians_predictions_df.pkl)
        - [Error evaluations](data/processed/errors_df.pkl)
    - [Works in Progress Folder](data/wip)
    
- [SRC:](src)
    - [Python Initilization file](src/__init__.py)
    - [Script for Data Cleaning](src/data_cleaning.py)
    - [Script for Modeling](src/modeling.py)
        
- [FIGURES:](figures)
    - Visualizations used/created throughout the project.
    
- [MODELS:](models)
    - Pickled files storing data relevant to the model creation.

- [NOTEBOOKS:](notebooks)
    - [Preliminary Exploratory Data Analysis](notebooks/eda-prelim.ipynb)
    - [EDA for Models](notebooks/eda-models.ipynb)
    - [Models](notebooks/models.ipynb)
    - [Visualizations](notebooks/visualizations)

- [PRESENTATION:](presentation)
    - [PDF](presentation/mod_4_real_estate_project.pdf)
    - [Powerpoint](presentation/mod_4_project.pptx)

## Business Understanding

The  business context for this project is relatively straightforward - select 5 top zip codes for investment within the United States, based on a dataset given from Zillow.

**GOAL: Predict top 5 zip code in United States for real estate firm to invest in.**

To further clarify this goal, we use a risk-adjusted Return on Investment (ROI) as our metric for "top":

- **ROI:** Predicted Price Increase / Initial Investment
- **Risk-adjustment:** After some exploratory data analysis (EDA), we define risk-adjusted by limiting the range of zip codes to those without large ranges of error in the model prediction.

***

## Data Understanding

The dataset for this project came from Zillow, with the following data from 1996 through 2018:
- RegionID (Zip Code)
- RegionName (Zillow-defined code)
- City
- State
- Metro (Metropolitan Area)
- CountyName
- Size Rank (Ordinal City size categories)
- Monthly Median Prices

An overview of the dataset:


```python
import pandas as pd
df = pd.read_csv('data/raw/zillow_data.csv')
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>RegionID</th>
      <th>RegionName</th>
      <th>City</th>
      <th>State</th>
      <th>Metro</th>
      <th>CountyName</th>
      <th>SizeRank</th>
      <th>1996-04</th>
      <th>1996-05</th>
      <th>1996-06</th>
      <th>...</th>
      <th>2017-07</th>
      <th>2017-08</th>
      <th>2017-09</th>
      <th>2017-10</th>
      <th>2017-11</th>
      <th>2017-12</th>
      <th>2018-01</th>
      <th>2018-02</th>
      <th>2018-03</th>
      <th>2018-04</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>84654</td>
      <td>60657</td>
      <td>Chicago</td>
      <td>IL</td>
      <td>Chicago</td>
      <td>Cook</td>
      <td>1</td>
      <td>334200.0</td>
      <td>335400.0</td>
      <td>336500.0</td>
      <td>...</td>
      <td>1005500</td>
      <td>1007500</td>
      <td>1007800</td>
      <td>1009600</td>
      <td>1013300</td>
      <td>1018700</td>
      <td>1024400</td>
      <td>1030700</td>
      <td>1033800</td>
      <td>1030600</td>
    </tr>
    <tr>
      <th>1</th>
      <td>90668</td>
      <td>75070</td>
      <td>McKinney</td>
      <td>TX</td>
      <td>Dallas-Fort Worth</td>
      <td>Collin</td>
      <td>2</td>
      <td>235700.0</td>
      <td>236900.0</td>
      <td>236700.0</td>
      <td>...</td>
      <td>308000</td>
      <td>310000</td>
      <td>312500</td>
      <td>314100</td>
      <td>315000</td>
      <td>316600</td>
      <td>318100</td>
      <td>319600</td>
      <td>321100</td>
      <td>321800</td>
    </tr>
    <tr>
      <th>2</th>
      <td>91982</td>
      <td>77494</td>
      <td>Katy</td>
      <td>TX</td>
      <td>Houston</td>
      <td>Harris</td>
      <td>3</td>
      <td>210400.0</td>
      <td>212200.0</td>
      <td>212200.0</td>
      <td>...</td>
      <td>321000</td>
      <td>320600</td>
      <td>320200</td>
      <td>320400</td>
      <td>320800</td>
      <td>321200</td>
      <td>321200</td>
      <td>323000</td>
      <td>326900</td>
      <td>329900</td>
    </tr>
    <tr>
      <th>3</th>
      <td>84616</td>
      <td>60614</td>
      <td>Chicago</td>
      <td>IL</td>
      <td>Chicago</td>
      <td>Cook</td>
      <td>4</td>
      <td>498100.0</td>
      <td>500900.0</td>
      <td>503100.0</td>
      <td>...</td>
      <td>1289800</td>
      <td>1287700</td>
      <td>1287400</td>
      <td>1291500</td>
      <td>1296600</td>
      <td>1299000</td>
      <td>1302700</td>
      <td>1306400</td>
      <td>1308500</td>
      <td>1307000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>93144</td>
      <td>79936</td>
      <td>El Paso</td>
      <td>TX</td>
      <td>El Paso</td>
      <td>El Paso</td>
      <td>5</td>
      <td>77300.0</td>
      <td>77300.0</td>
      <td>77300.0</td>
      <td>...</td>
      <td>119100</td>
      <td>119400</td>
      <td>120000</td>
      <td>120300</td>
      <td>120300</td>
      <td>120300</td>
      <td>120300</td>
      <td>120500</td>
      <td>121000</td>
      <td>121500</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 272 columns</p>
</div>



The nationwide median price looked like this:

![Nationwide Median](figures/nationwide.png)

**Data Analysis**
- Given the monthly price measurements, we used **Time Series Analysis** to gain a better understanding for the patterns in the data that would impact our predictions.

- Additionally, we restrict our model construction to data ***after the 2008 recession,*** since the variation due to the anomaly is already known, and our model will perform better without having to account for such a huge fluctuation.

- Finally, given computational resource restrictions, we ***limit our dataset*** to the 60 zip codes with the largest ROI in a 5-year rolling window.

## Predictive Analysis

### Time Series Analysis
By using time-series analysis, we can use time-linked historical data to discover which areas have the highest ROI, which is a time-delta linked indicator. This particular method enables median price value prediction.

In order to use this model, we must eliminate noise in the data in order to make accurate predictions, based on the assumptions of the model:

1. **Stationarity** - Ensures that the distribution of data does not change over time

2. **Seasonality** - Adjusting for regular fluctuations based on a fixed interval (e.g., higher prices in spring, lower prices in fall)

3. **Autocorrelation** - Adjusts for covariance of time-series with itself, based on its variables.

4. **Trend** - Adjusts for long-term trends such as overall increase, overall decrease.

The goal of these limitations is to remove the time-based impacts upon the median price to discover any potential underlying patterns in the data.

### Performance Metric


###  Model Selection




## Conclusions



### Recommendations:

1. Higher Median Investment

2. Lower Median Investment

### Areas for Growth:

#### Include Adjacent Data Resources
With additional time, we would incorporate other ways to measure "top 5" and ROI, including usin other sources like:
- Zillow Rent Data
- Competitor Median Prices
- AirBnB rental increases/returns

#### Improve Model
The model was significantly limited due to time and resource constraints. With more of each, we could:
- Fit model to all zip codes, not just limited set
- Consider grouping zip codes and areas into better tiers
- Train model on nationwide data for the ability to "drill-down" more precisely

#### Extend Time Frame for Analysis
With more data, we could predict longer term trends instead of just the limited 5-year period we selected.


## Project Info

Contributors: __[Alexander](https://www.linkedin.com/in/anewt/)__ __[Newton](https://github.com/anewt225)__, __[Jake](https://www.linkedin.com/in/jake-miller-brooks-a37a64106//)__ __[Miller Brooks](https://github.com/jmillerbrooks)__

Languages  : Python

Tools/IDE  : Git, Command Line (Windows), Anaconda, Jupyter Notebook / Jupyter Lab, Google Slides

Libraries  : numpy, pandas, matplotlib, seaborn, scikit-learn, statsmodels 

Duration   : August 2020
Last Update: 08.24.2020


```python

```

