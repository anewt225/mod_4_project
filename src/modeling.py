import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


def RMSE(y_true, y_pred, last_only=True):
    """Simple wrapper function on mean_squared_error to return RMSE
    
    Params:
        predictions (series or array like object), the predicted values from model
        test_data (series or array like object), the true target values
        
    Returns:
        RMSE (list) list of accumulated RMSE values for each observation in consecutive time order
        i.e. the first return value will be just the error of first prediction, second the sqrt of mean squared error for first 2 predictions, etc."""

    
    # Ensure predictions and test_data are same size
    if len(y_pred) != len(y_true):
        return "Test data and predictions must have equal length"
    
    elif last_only == False:
        rmse = [mean_squared_error(y_true[:i+1], y_pred[:i+1], squared=False) for i, _ in enumerate(y_pred)]
        return rmse
    else:
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        return rmse
    
def test_stationarity(series):
    """Simple wrapper around adfuller that prints in more readable format
    
    Params:
        series (series) a timeseries
    Returns:
        adfuller test result"""
    
    result = adfuller(series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
    return result

def get_diff_param(series):
    """Suggests a starting point for the d parameter of a SARIMAX/ARIMA model order(p,d,q)
    
    Params:
        (series) a timeseries
        
    Returns:
        (int) suggested starting point for d parameter of the order call to SARIMAX/ARIMA model"""
    
    d = -1
    p_val = 1
    a_fuller = None
    
    # run adfuller on series, save p_val, increment d, difference the series and run again until p_val <= .05
    while p_val > .05:
        a_fuller = test_stationarity(series)
        p_val = a_fuller[1]
        d += 1
        series = series.diff()[1:]
    
    return d

def n_month_roi(series, n):
    """Return roi for preceding n months zipcode dataframe, returning zero if na denominator values
    
    Params: series
    Returns: (float) ROI for preceding five years, or 0 if na_values n months back"""
    
    start_val = series[-n]
    end_val = series[-1]
    
    # Return zero if na value n months ago
    if np.isnan(start_val):
        return 0
    # Otherwise return ROI for the n month period
    else:
        total_return = end_val - start_val
        roi = total_return / start_val
        return roi
    
def n_month_std(series, n):
    
    """Return standard deviation for preceding n months of zipcode dataframe column, returning zero if na denominator values
    
    Params: series
    Returns: (float) std for preceding five years"""
    
    start_val = series[-n]
    
    
    # Return zero if na value n months ago
    if np.isnan(start_val):
        return 0
    
    else:
        return series[-n:].std()
    
def error_as_pct(rmse, start_val, end_val):
    """Compute the error (rmse) as a percentage of the total change in value
    
    Params: rmse(float) the residual mean squared error of a forecast, start_val(float) the starting value in from the month before 
        forecasting begins, end_val(float) the last value of the forecast
        
    Returns:
        (float) rmse as a percentage of total change between start and end of forecast"""
    
    total_delta = end_val - start_val
    error_pct = rmse / total_delta
    return error_pct

def hw_rmse(series):
    """Simple wrapper that fits holtwinters model and returns RMSE for the predictions
    
    Params: (series) a timeseries to model
    
    Returns: rmse (float) the raw RMSE, rmse_pct (float) the RMSE represented as a percentage of total change in value"""
    

    X = series[-108:]

    # set trainset to include all but last 48 months (4 years) only training on data between 9-4 years ago
    train_size = int(len(X) - 48)
    train, test = X[-108:train_size], X[train_size:]


    model = ExponentialSmoothing(train, trend='add', seasonal='add', freq='MS')

    results = model.fit()

    # Predict 48 months from end of train set
    forecast = results.predict(start=test.index[0], end=test.index[-1])
    
    rmse = RMSE(test, forecast)
    rmse_pct = error_as_pct(rmse, train[-1], test[-1])
    return (rmse, rmse_pct)

def SARIMAX_error(series, p=10, d=2, q=2):
    """Simple wrapper that fits SARIMAX model and returns RMSE (raw and pct) for the predictions, confidence interval, start of forecast and end of actual 
    values"""
    
    
    X = series
    
    # set trainset to include all but last 48 months (4 years) only training on data between 9-4 years ago
    train_size = int(len(X) - 48)
    train, test = X[-108:train_size], X[train_size:]

    model = SARIMAX(train, order=(p,d,q), freq='MS',  initialization='approximate_diffuse')

    results = model.fit()

    # Predict 48 months from end of train set
    forecast = results.get_forecast(steps=48)
    pred_ci = forecast.conf_int(alpha=.05)

    predictions = forecast.predicted_mean

    rmse = RMSE(test, predictions)
    pct = error_as_pct(rmse, train[-1], test[-1])
    
    return pred_ci, rmse, pct, (train[-1], test[-1])

def plot_acf_pacf(series):
    plt.figure(figsize=(15,10))
    plt.subplot(211)
    plot_acf(series, lags=48, ax=plt.gca())
    plt.subplot(212)
    plot_pacf(series, lags=48, ax=plt.gca())
    plt.show()