import streamlit as st 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np 
from functions import * 



st.header("Welcome to your real estate accelerator")
uploaded_file = st.file_uploader(label="Upload **Stessa Transactions** Data .csv", type=['.csv'])
if uploaded_file is not None:
    df_main = pd.read_csv(uploaded_file)
    st.write('')
    uploaded_file2 = st.file_uploader(label="Upload **Rent Charges** Data .csv", type=['.csv'])
    

    if uploaded_file2 is not None:
        start_date = st.sidebar.date_input("Start date")
        start_date = pd.to_datetime(start_date)
        # * Fromat is datetime year month day 2023-03-04
        end_date = st.sidebar.date_input("End date")
        df_rent = pd.read_csv(uploaded_file2)
        end_date = pd.to_datetime(end_date)
        # INSTERT FILTERING CODE 
        df_main = df_datetime(df_main)
        # * Collections Rate 
        df_rent_pct = filter_rent_collection(df_main, df_rent, start_date = start_date, end_date = end_date) 
        df_rent_output, collection_rate = rents_output_filter(df_rent_pct)
        # * Monthly Expenses 
        df_expenses = filter_variable_costs(df_main, start_date, end_date)
        df_mean_expenses = monthly_avg_expenses(df_expenses, start_date = start_date, end_date = end_date)
        df_expenses_output, mo_expenses = expenses_output_filter(df_mean_expenses)
        # OUTPUT VALUES FOR METRICS
        with st.spinner('Updating Report...'):
            m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
            m1.metric(label ='Collection Rate',value = collection_rate)
            m2.write('')
            m3.metric(label ='Avg Monthly Expenses Per Property',value = mo_expenses)
            m4.write('')
            m5.metric(label = 'Avg Lease Life Per Property', value = 3)
            
            m1, m2, m3 = st.columns((1,1,1))
            m1.write(df_rent_output)
            m2.write(df_expenses_output)
            m3.write(df_rent)

    else: 
       pass 

    # df_main = pd.read_csv(uploaded_file)
    # st.write(df_main)
    # df_main = df_datetime(df_main)

# st.write('')
# uploaded_file2 = st.file_uploader(label="Upload **Rent Charges** Data .csv", type=['.csv'])
# if uploaded_file2 is not None: 
#     df_rent = pd.read_csv(uploaded_file2)
#     st.write(df_rent)
#     df_rent = df_rent_datetime(df_rent)

# avg_mo_expenses_pp = 5 
    