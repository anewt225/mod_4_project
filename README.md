# mod_4_project
Flatiron Mod 4 Time-Series Real Estate Project
## The Process

These steps are informed by the CRISP-DM process.

### 1. Getting Started

Please start by reviewing this document. If you have any questions, please ask them in Slack ASAP so (a) we can answer the questions and (b) so we can update this repository to make it clearer.

### 2. CRISP-DM Check-In pt.1 - Monday
You will meet with your instructors on Monday to “pitch” your project idea. We will be focusing on the steps of the CRISP-DM model.  Be prepared to answer the following questions. Be prepared to answer the following questions:


- Business Understanding
	- What is the business problem?
        - Consulting for real estate company to find top 5 zip codes to invest in
        - What is meant by zip code? Eg., are you looking for neighborhoods, cities, etc.?

	- What questions will you be addressing?
        - How to define top 5?
        - What's relevant to investment?
        - How does risk of loss compare over 5 year windows relative to areas of high return?
        - Time-permitting - how much risk can be mitigated with cumulative value of expected rent over projected period of investment?
        - How would recommendations have changed over time? I.e, would we have given same 5 zipcodes 10 years ago?
        
   - Have you clearly defined your goal for your analysis?
        - Output 5 zipcodes with best Risk-adjusted return
        
   - Have your thought about who your audience is and how they would use this information?
       - Audience is real-estate firm.
       - They should use this information to determine where to begin search for investment properties
       
   - How does this help the goals of the business/organization?
       - Helps increase return by predicting most effective areas of investment.
   
- Data Understanding
   - What data are you using?
       - Data available from zillow (given), expected rent data (time-permitting)
       
   - How does your data help you answer the business question?
       - Data has price, time, and zipcodes, so should help in predicting values
       
   - How many observations does your dataset contain?
       - 3,744,704
       
   - What is the distribution of your data?
       - count      14723.00000
mean      305870.27100
std       387052.96398
min        22200.00000
25%       138200.00000
50%       212900.00000
75%       353300.00000
max     19314900.00000
   - What data types do you have?
       - Datetimes, Floats
       
       
- Data Preparation
   - Have you looked/dealt with missing values?
       - not yet
   - Have you done any data-type conversion?
      - Yes - to_datetime
      
   - Does your data contain any outliers or non-sensical values?
       - Yes, prices are not evenly distributed across US, requires further investigation
       
       
   
   
### 3. CRISP-DM Check-In pt.2 - Tuesday
- EDA/Visualization
   - What visualizations have you already made/planning to make?
       
       - Chloropleth Map of Growth By Zipcode
       - Predicted price growth with confidence intervals
       - Box/whiskers or violinplot for range and median price over five year interval for top five zipcodes selected
       
   - What messages are these visualizations trying to convey?
   
       - Which areas have high value growth
       - The band of confidence for our predictions
       - Both the range of prices within the zipcodes and also how similar the price information is across the zipcodes
       
   - What visualizations have you already made/planning to assess if your data meets the assumtions of linear regression?
       
       - We will be making ACF/PACF plots
       - Seasonal/Trend Decomposition Plots
       - Our data will not meet the assumptions of linear regression as the basis for our analysis is that the features have strong autocorrelation
       
- Modeling:
    - Is this a classification task? A regression task? Something else?
    
        - This is a form of regression as applied in timeseries modeling
        
    - What models will we try?
    
        - We will be trying ARIMA, ARMA, AR, and maybe SARIMA models
        
    - How do we deal with overfitting?
    
        - We will attempt to use the narrowest windows possible that yield good results
        - Likewise we will do our best to difference our series as little as possible
        
    - Do we need to use regularization or not?
        
        - Some measure of regularization is typical when working with time series data, especially since the series we are working with are largely non-stationary
        
    - What sort of validation strategy will we be using to check that our model  - works well on unseen data?
    
        - We will be validating first on the most recent 25% of the dataset, and time permitting will acquire additional updated data from zillow on which to test our models
        
    - What loss functions will we use?
    
        - We will use Residual Mean Squared Error on growth rate, and time permitting will also weight RMSE by the upper and lower bands of a 95% confidence interval
        
    - What threshold of performance do we consider as successful?
    
        - This is an excellent question, would love to hear your thoughts on what is reasonable given the scope of this project.
            
           - Some thresholds or baseline measures we have considered are a simple rolling lag over five year period, also possible would be whether or not our recommendations would beat a historical five year return on the S&P 500 with some adjustment for tax advantage of real estate holdings over cap gains.

- Evaluation:
    - How are you determining which variables are important.
    
        - We have a very limited number of variables. And little room for engineered features given this dataset.
        
    - What overall metric of success are you using.
    
        - Please see above responses regarding performance threshold and loss function
        
    - What additional steps might you need to take to improve the model? (ex: transforming data, scaling data, getting more features) 
    
        - We may attempt the same models on effective growth rate i.e. observation/lagged observation - 1
        - Would love to hear your insights on feature scaling in timeseries
        - We may also add rent data if our MVP performs, as the same technique should scale well to similarly formatted data available from zillow
        - Unlikely to have enough time to attempt this approach, but if there is time, may attempt LSTM model.
   
### 4. MVP Checkin - Wednesday
You will meet with an instructor who will check if the minimum requirements of the project are completed. AAt this point you should have a "best" model that "works" in answering the business question but may need some final adjustments.  Following this meeting you should be ready to polish your notebook and work on your slidedeck.


### 5. Practice Presentations- Thursday
You do a practice presentation in front of the class.  At this point the instructors and other students will provide verbal feedback which can be incorportated in your final presentation.

### 6. Project Presentations- Friday
You will present your project to the class using your slidedeck.  This presentation should not take more than 5 minutes and should be directed towards a non-technical audience.  Both partners should participate in the presentation of the project.

## Grading Rubric

The grading rubric for the project can be found [here](https://docs.google.com/spreadsheets/d/1hbIZUQN2qipZZQsgMQRdBKvsTYRace4r09xkgKvmW_E/edit?usp=sharing).
