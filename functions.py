import pandas as pd
import numpy as np 
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import math


def df_datetime(df):
  df['date'] = pd.to_datetime(df['Date'])
  return df 


# * VARIABLE COSTS FUNCTIONS 

def filter_variable_costs(df, start_date, end_date):
  '''
  this function finds the monthly average variable costs, and standard deviaton for the monthly average variable cost 
  parameters: df = main dataframe with transactions, start_date, end_date
  returns: df = df with total amounts corresponding to every month and category
              - this will allow me to find the mean and standard deviation of each category
  '''
  filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
  filtered_df = filtered_df[(filtered_df['Category'] == 'Utilities') | (filtered_df['Category'] == 'Repairs & Maintenance') | 
                          (filtered_df['Category'] == 'Legal & Professional') | (filtered_df['Category'] == 'Capital Expenses')
                          | (filtered_df['Category'] == 'Taxes')]
  filtered_df["month_name"] = filtered_df["date"].apply(lambda x: x.strftime("%B"))
  filtered_df["month"] = filtered_df["date"].apply(lambda x: x.strftime("%m"))
  filtered_df["year"] = filtered_df["date"].apply(lambda x: x.strftime("%Y"))
  filtered_df = filtered_df.groupby(by=["month","year","Category"],as_index=False)['Amount'].sum()
  filtered_df = filtered_df.sort_values(['year', 'month']).reset_index(drop=True)
  return filtered_df

def monthly_avg_expenses(df, start_date, end_date):
  ''''
  Input: df with filtered variable costs, from filtered_variable_cost function 
  Output: df with mean expenses for each year, month, property combo
  I should just be able to combine these functions eventually
  '''
  filtered_df = df.groupby(by='Category',as_index=False)['Amount'].sum()
  recent_full_month = (end_date + timedelta(days=10))
  filtered_df['number_months'] = recent_full_month.month - start_date.month + 12*(recent_full_month.year - start_date.year)
  filtered_df['mean'] = round((filtered_df['Amount'] / filtered_df['number_months']),2)
  return filtered_df

def expenses_output_filter(df):
  '''
  Input: the df from monthly_avg_expenses
  Output: df with mean expenses per property for the time period and the mean expenses for the time period
  '''
  df_filtered = df.drop(columns=['Amount','number_months'])
  df_filtered = df_filtered.rename(columns={'mean':'Total'})
  df_filtered['Total'] = df_filtered['Total'] * -1
  df_filtered = df_filtered.sort_values(by='Total', ascending=False).reset_index()
  df_filtered = df_filtered.drop(columns=['index'])
  mean_total = df_filtered['Total'].sum()
  add_dollar_sign = lambda x: '${:,.2f}'.format(x)
  df_filtered['Total'] = df_filtered['Total'].apply(add_dollar_sign) 
  

  return df_filtered, mean_total

# * COLLECTION RATE FUNCTIONS 

def filter_rent_collection(df_main, df_rents, start_date, end_date):
  ''' 
  this df will find the vacancy rate that the properties are perfoming at. Vacancy Rate is also the inverse of Collections Rate
  input: df_main = main stessa transactions df, df_rents = df with the rents charged for each property for each month (NEED TO FIND HOW TO GET THIS)
  start_date, end_date (IN FUTURE WILL MAKE MOVE WITH SLIDER)
  output: df with year and months that rent was charged, and how much was collected --> will find summary statistics from there
  '''
  filtered_df = df_main[(df_main['date'] >= start_date) & (df_main['date'] <= end_date)]
  filtered_df = filtered_df[(filtered_df['Category']=='Income')]
  
  # todo: maybe add a late fee counter? and account for in collection rate for late fees
  
  filtered_df["month"] = filtered_df["date"].apply(lambda x: x.strftime("%m"))
  filtered_df["year"] = filtered_df["date"].apply(lambda x: x.strftime("%Y"))
  filtered_df = filtered_df.groupby(by=['month', 'year','Property'],as_index=False)['Amount'].sum()
  filtered_df = filtered_df.rename(columns={'Amount':'rent_collected'}) 
  filtered_df['year'] = filtered_df['year'].astype(str)
  df_rents['year'] = df_rents['year'].astype(str)
  filtered_df['month'] = filtered_df['month'].astype(str)
  df_rents['month'] = df_rents['month'].astype(str)
  filtered_df['month'] = filtered_df['month'].str.lstrip('0')
  df_rents['month'] = df_rents['month'].str.lstrip('0')

  # Todo: NEED TO FIGURE OUT HOW TO ADD A ZERO FOR A PROPERTY IF IT HAD NO RENT COLLECTED FOR THAT YEAR

  filtered_df = pd.merge(filtered_df, df_rents,  on=['Property','month','year']) 
  filtered_df['pct_rent_collected'] = filtered_df['rent_collected'] / filtered_df['rent_charged']
  return filtered_df
# ! 3/6/23 right now the output is mising anyproperties that reported 0 rent for the months 

def rents_output_filter(df_rents):
    '''
    Input: df from filter_rent_collection 
    Output: df with mean rent collection per property 
    '''
    filtered_df = df_rents.drop(columns=['year','month','rent_collected','rent_charged']) 
    filtered_df = filtered_df.groupby(by=['Property']).mean('pct_rent_collected').reset_index()
    collection_rate = filtered_df['pct_rent_collected'].mean()
    filtered_df = filtered_df.sort_values(by='pct_rent_collected', ascending=True).reset_index()
    filtered_df = filtered_df.drop(columns=['index'])

    return filtered_df, collection_rate