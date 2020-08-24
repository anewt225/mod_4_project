import pandas as pd
import numpy as np


def load_clean_zillow_data():
    '''
    runs sequentially:
        load_raw_zillow() 
            - loads zillow_data.csv
        
        df = drop_df_columns(df) 
            - drops extraneous columns
        
        df = melt_df(df)
            - consolidates times/values into two columns 'time' and 'value'
            
        df= zipcode_columns(df)
            - pivots the df into a df of timeseries by zipcode
            
    result:
        zillow_data.csv loaded and cleaned
        na values induced in the pivot step are retained, columns may still
        be useful in some form as length of forecast is not yet decided
    '''
    
    
    df = load_raw_zillow()
    df = drop_df_columns(df)
    df = melt_df(df)
    df = zipcode_columns(df)
    

    
    return df



def drop_df_columns(frame):
    '''
    data cleaning: drop columns
    
    input: 
        frame: dataframe
        
    output: frame w/o the RegionID and SizeRank columns
    '''
    frame = frame.drop(['RegionID', 'SizeRank'], axis=1)
    return frame

def melt_df(frame):
    '''
    data transformation: consolidate all date columns into one column,
    values for each datetime for each RegionName into separate column
    dropping na vals in the value column
    
    input: dataframe 
    output: dataframe w/ datetime columns and values consolidated into two columns 'time' and 'value'
    '''
    
    melted = pd.melt(frame, id_vars=['RegionName', 'City', 'State', 'Metro', 'CountyName'], var_name='time')
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    melted = melted.dropna(subset=['value'])
    
    return melted



def zipcode_columns(frame):
    '''
    data transformation: pivot the zipcodes to columns yielding a dataframe of timeseries by zipcode
    
    input: melted dataframe
    output: dataframe of timeseries by zipcode
    '''
    zip_df = frame.pivot_table(index='time', columns='RegionName', values='value')
    # Convert columns to string for easier index access, this also removes the RegionName column index
    zip_df.columns = [str(x) for x in zip_df.columns]
    return zip_df



def load_raw_zillow():
    
    '''
    loads in zillow_data.csv from github repo using pd.read_csv
    
    outputs: dataframe of zillow_data.csv
    '''
    
    df = pd.read_csv('https://raw.githubusercontent.com/learn-co-students/dc-ds-060120/master/mod-4/week-3/Mod_4_Project/time-series/zillow_data.csv')
        
    return df