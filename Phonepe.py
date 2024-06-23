import os
import json
import pandas as pd
import mysql.connector
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from PIL import Image

# Connection With MySQL :

mydb = mysql.connector.connect(host = "127.0.0.1",
                               port = "3306",
                               user = "root",
                               password = "Ramya$125",
                               database = "Phonepe")
cursor = mydb.cursor(buffered=True)

# Extracting DataFrames From MySQL:

# Aggregated Insurance :

cursor.execute(" SELECT * FROM aggregated_insurance")
mydb.commit()
table = cursor.fetchall()

Agg_Insur = pd.DataFrame(table ,columns = ['States','Years','Quarters','Transaction_Type','Transaction_Count','Transaction_Amount'])

# Aggregated Transaction :

cursor.execute(" SELECT * FROM aggregated_transaction")
mydb.commit()
table = cursor.fetchall()

Agg_Tran = pd.DataFrame(table ,columns = ['States','Years','Quarters','Transaction_Type','Transaction_Count','Transaction_Amount'])

# Aggregated User :

cursor.execute(" SELECT * FROM aggregated_user")
mydb.commit()
table = cursor.fetchall()

Agg_User = pd.DataFrame(table ,columns = ['States','Years','Quarters','Brands','Transaction_Count','Percentage'])

# Map Insurance :

cursor.execute(" SELECT * FROM map_insurance")
mydb.commit()
table = cursor.fetchall()

Map_Insur = pd.DataFrame(table ,columns = ['States','Years','Quarters','Districts','Transaction_Count','Transaction_Amount'])

# Map Transaction :

cursor.execute(" SELECT * FROM map_transaction")
mydb.commit()
table = cursor.fetchall()

Map_Tran = pd.DataFrame(table ,columns = ['States','Years','Quarters','Districts','Transaction_Count','Transaction_Amount'])

# Map User :

cursor.execute(" SELECT * FROM map_user")
mydb.commit()
table = cursor.fetchall()

Map_User = pd.DataFrame(table ,columns = ['States','Years','Quarters','Districts','Registered_Users','App_Opens'])

# Top Insurance :

cursor.execute(" SELECT * FROM top_insurance")
mydb.commit()
table = cursor.fetchall()

Top_Insur = pd.DataFrame(table ,columns = ['States','Years','Quarters','Pincodes','Transaction_Count','Transaction_Amount'])

# Top Transaction :

cursor.execute(" SELECT * FROM top_transaction")
mydb.commit()
table = cursor.fetchall()

Top_Tran = pd.DataFrame(table ,columns = ['States','Years','Quarters','Pincodes','Transaction_Count','Transaction_Amount'])

# Top User :

cursor.execute(" SELECT * FROM top_user")
mydb.commit()
table = cursor.fetchall()

Top_User = pd.DataFrame(table ,columns = ['States','Years','Quarters','Pincodes','Registered_Users'])

# Transaction Amount And Count Based On Years :

def tran_amount_count_year(df, year):

    tacy = df[df['Years'] == year]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby('States')[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1 :    
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_Amount", title = f"{year} => Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.turbid_r, height = 400, width = 480)
        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_Count", title = f"{year} => Transaction Count",
                            color_discrete_sequence= px.colors.sequential.turbid_r, height = 400, width = 480)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        
        response = requests.get(url)
        data = json.loads(response.content)
        states_name = []
        for feature in data['features']:
            states_name.append(feature['properties']['ST_NM'])
        states_name.sort()
    
    
        fig_india_1 = px.choropleth(tacyg, geojson = data, locations = "States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_Amount", color_continuous_scale="turbid",
                                    range_color = (tacyg["Transaction_Amount"].min(),tacyg["Transaction_Amount"].max()),
                                    hover_name = "States", title = f"{year} => Transaction Amount",
                                    fitbounds = "locations", height = 500, width = 500)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
    with col2 :
        fig_india_2 = px.choropleth(tacyg, geojson = data, locations = "States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_Count", color_continuous_scale="turbid",
                                    range_color = (tacyg["Transaction_Count"].min(),tacyg["Transaction_Count"].max()),
                                    hover_name = "States", title = f"{year} => Transaction Count",
                                    fitbounds = "locations", height = 500, width = 500)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return tacy 

# Transaction Amount And Count Based On Quarters :

def tran_amount_count_quarter(df, quarter):

    tacy = df[df['Quarters'] == quarter]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby('States')[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
    
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_Amount", title = f"Year :{tacy['Years'].min()}  Quarter:{quarter} => Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Pinkyl_r,height = 400, width = 480)
        st.plotly_chart(fig_amount)
    
    with col2 :
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_Count", title = f"Year :{tacy['Years'].min()}  Quarter:{quarter} => Transaction Count",
                            color_discrete_sequence= px.colors.sequential.Pinkyl_r,height = 400, width = 480)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1 :
    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        
        response = requests.get(url)
        data = json.loads(response.content)
        states_name = []
        for feature in data['features']:
            states_name.append(feature['properties']['ST_NM'])
        
        states_name.sort()
        
        fig_india_1 = px.choropleth(tacyg, geojson = data, locations = "States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_Amount", color_continuous_scale="tealrose",
                                    range_color = (tacyg["Transaction_Amount"].min(),tacyg["Transaction_Amount"].max()),
                                    hover_name = "States", title = f"Year :{tacy['Years'].min()}  Quarter:{quarter} => Transaction Amount",
                                    fitbounds = "locations", height = 500, width = 500)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2 :
        fig_india_2 = px.choropleth(tacyg, geojson = data, locations = "States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_Count", color_continuous_scale="tealrose",
                                    range_color = (tacyg["Transaction_Count"].min(),tacyg["Transaction_Count"].max()),
                                    hover_name = "States", title = f"Year :{tacy['Years'].min()}  Quarter:{quarter} => Transaction Count",
                                    fitbounds = "locations", height = 500, width = 500)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return tacy

# Aggregated Transaction , Transaction Type Based On States :

def agg_tran_tran_type (df, state ):
    tacy= df[df['States'] == state]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby('Transaction_Type')[['Transaction_Count','Transaction_Amount']].sum()
    tacyg.reset_index( inplace = True)

    col1, col2 = st.columns(2)
    with col1 :
        fig_pie_1 = px.pie(data_frame = tacyg, width=800,names = "Transaction_Type", values = "Transaction_Amount",
                            title = f"{state } => Transaction Amount", hole=0.4, color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_pie_1)

    with col2 :
        fig_pie_2 = px.pie(data_frame = tacyg, width=800,names = "Transaction_Type", values = "Transaction_Count",
                            title = f"{state} => Transaction Count", hole=0.4,color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_pie_2)

# Aggregated User Brands Transaction Count Based On Year:

def agg_user_brand_count_y(df, year):
    aguy = df[df['Years'] == year]
    aguy.reset_index(drop = True, inplace = True)
    
    aguyg = pd.DataFrame(aguy.groupby('Brands')["Transaction_Count"].sum())
    aguyg.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(aguyg, x = "Brands", y = "Transaction_Count", title = f"{year} => Brands And Transaction Count",
                       width = 1000, height = 500,color_discrete_sequence=px.colors.sequential.Sunset_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

# Aggregated User Brands Transaction Count Based On Year And Quarter :

def agg_user_brand_count_quarter(df, quarter):
    
    aguyq = df[df['Quarters'] == quarter]
    aguyq.reset_index(drop = True, inplace = True)
    
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")['Transaction_Count'].sum())
    aguyqg.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(aguyqg, x = "Brands", y = "Transaction_Count", title = f"Year:{df['Years'].min()}  Quarter:{quarter} => Brands And Transaction Count",
                           width = 1000, height = 500,color_discrete_sequence=px.colors.sequential.Sunset_r, hover_name = "Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

# Aggregated User Brands And Percentage Based On State:

def agg_user_brand_count_state(df, state):
    auyqs = df[df['States']== state]    
    auyqs.reset_index(drop = True, inplace = True) 
    
    fig_line_1 = px.line(auyqs, x = "Brands", y = "Transaction_Count" ,title = f"Year:{df['Years'].min()}  State:{state} => Brands, Transaction Count And Percentage", 
                         width = 1000,height = 500, hover_data = ['Percentage'], markers = True)
    st.plotly_chart(fig_line_1)

# Map Insurance District Transaction Amount And Count based on state  :

def map_insur_dist(df, state ):
    tacy= df[df['States'] == state]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby("Districts")[['Transaction_Count','Transaction_Amount']].sum()
    tacyg.reset_index( inplace = True)

    col1, col2 = st.columns(2)
    with col1 :
        fig_bar_1 = px.bar(tacyg, x = "Transaction_Amount", y = "Districts", orientation= 'h', color_discrete_sequence=px.colors.sequential.Mint_r,
                        title = f"State : {state} => District Wise Transaction Amount", height = 500)
        st.plotly_chart(fig_bar_1)
    with col2 :
        fig_bar_2 = px.bar(tacyg, x = "Transaction_Count", y = "Districts", orientation= 'h', color_discrete_sequence=px.colors.sequential.Mint_r,
                        title = f"State : {state} => District Wise Transaction Count", height = 500)
        st.plotly_chart(fig_bar_2)

# Map User Registered User And App Opens based on Year, Group By States: 

def map_user_year(df, year):
    muy = df[df['Years'] == year]
    muy.reset_index(drop = True, inplace = True)
    
    muyg = muy.groupby('States')[["Registered_Users", "App_Opens"]].sum()
    muyg.reset_index(inplace = True)
    
    fig_line_1 = px.line(muyg, x = "States", y = ["Registered_Users","App_Opens" ],width = 1000,height = 800,markers = True,
                         title = f"Year:{year} => Registered Users And App Opens ",color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muy

# Map User Registered User And App Opens based on Quarter, Group By States: 

def map_user_quarter(df, quarter):
    muyq = df[df['Quarters'] == quarter]
    muyq.reset_index(drop = True, inplace = True)
    
    muyqg = muyq.groupby('States')[["Registered_Users", "App_Opens"]].sum()
    muyqg.reset_index(inplace = True)
    
    fig_line_1 = px.line(muyqg, x = "States", y = ["Registered_Users","App_Opens" ],width = 1000,height = 800,markers = True,
                         title = f"Year:{df['Years'].min()}  Quarter:{quarter} => Registered Users And App Opens ",color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_line_1)
    return muyq
        
# Map User Registered Users And App Opens Based On States And Districts :

def map_user_state_district(df, state):
    muyqs = df[df['States'] == state]
    muyqs.reset_index(drop = True, inplace = True)

    fig_bar_1 = px.bar(muyqs, x = "Registered_Users", y= "Districts",color_discrete_sequence= px.colors.sequential.Rainbow,
                       title = f"Year:{df['Years'].min()}  State:{state} => Register Users",
                       height = 600,  orientation= 'h')
    st.plotly_chart(fig_bar_1)
    
    fig_bar_2 = px.bar(muyqs, x = "App_Opens", y= "Districts", color_discrete_sequence= px.colors.sequential.Sunsetdark_r,
                       orientation= 'h', title = f"Year:{df['Years'].min()}  State:{state} => App Opens",height = 500 )
    st.plotly_chart(fig_bar_2)

# Top Insurance State,Quarters And Pincodes Wise Transaction Amount And Count : 

def top_insur_quarter_state(df, state):
    tiy = df[df['States'] == state]
    tiy.reset_index(drop = True, inplace = True)

    col1, col2= st.columns(2)
    with col1 :
        fig_bar_1 = px.bar(tiy, x = "Quarters", y= "Transaction_Amount",  title = f"Year:{df['Years'].min()}  Transaction Amount", hover_data = ["Pincodes"],
                        height = 600, width = 500,color_discrete_sequence= px.colors.sequential.Peach_r)
        st.plotly_chart(fig_bar_1)
    with  col2:
        fig_bar_2 = px.bar(tiy, x = "Quarters", y= "Transaction_Count", title = f"Year:{df['Years'].min()}  Transaction Count",hover_data = ["Pincodes"],
                        height = 600, width = 500,color_discrete_sequence= px.colors.sequential.Greens_r)
        st.plotly_chart(fig_bar_2)

# Top User States, Quarters And Registered Users Based On Year :

def top_user_year(df, year):
    tuy = Top_User[Top_User['Years'] == 2020]
    tuy.reset_index(drop = True, inplace = True)
    
    tuyg =pd.DataFrame( tuy.groupby(['States','Quarters'])["Registered_Users"].sum())
    tuyg.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(tuyg, x = "States", y = "Registered_Users", color="Quarters",color_discrete_sequence=px.colors.sequential.Greens_r,
                       width = 1000, height = 800, title = f"Year:{df['Years'].min()}  => Registerd Users ", hover_name ='States')
    st.plotly_chart(fig_bar_1)
    return tuy

# Top User  Registerd Users , Pincodes And Quarters Based On State:

def top_user_state(df, state):
    tuys = df[df['States'] == state]
    tuys.reset_index(drop = True, inplace = True)
    
    fig_bar_1 = px.bar(tuys, x = "Quarters", y = "Registered_Users", title = f"State:{state} => Registerd Users , Pincodes And Quarters",
                       width = 1000, height = 800, color="Registered_Users",hover_data = ["Pincodes"],
                       color_continuous_scale= px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig_bar_1)

# Connection With MySQL :

def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(host = "127.0.0.1",
                                   port = "3306",
                                   user = "root",
                                   password = "Ramya$125",
                                   database = "Phonepe")
    cursor = mydb.cursor(buffered=True)
    
    # Plot 1 :
    
    query1 = f'''select States, sum(transaction_amount) as Transaction_Amount from {table_name}
                 group by states 
                 order by Transaction_Amount desc
                 limit 10;
                    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    
    df_1 = pd.DataFrame(table_1, columns=['States','Transaction_Amount'])

    col1, col2 = st.columns(2)
    with col1 :
        fig_amount_1 = px.bar(df_1, x = "States", y = "Transaction_Amount", title = " Top 10  =>  Transaction Amount", 
                                color_discrete_sequence= px.colors.sequential.Peach_r, height = 550,width = 500, hover_name = "States")
        st.plotly_chart(fig_amount_1)
    
    # Plot 2:
    
    query2 = f'''select States, sum(transaction_amount) as Transaction_Amount from {table_name}
                 group by states 
                 order by Transaction_Amount 
                 limit 10;
                    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=['States','Transaction_Amount'])

    with col2:
        fig_amount_2= px.bar(df_2, x = "States", y = "Transaction_Amount", title = "Last 10  =>  Transaction Amount",width = 600,
                                color_discrete_sequence= px.colors.sequential.Greens_r, height = 615, hover_name = "States")
        st.plotly_chart(fig_amount_2)
    
    # Plot 3:
    
    query3 = f'''select States, avg(transaction_amount) as Transaction_Amount from {table_name}
                 group by states 
                 order by Transaction_Amount ;
                    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    
    df_3 = pd.DataFrame(table_3, columns=['States','Transaction_Amount'])
    
    fig_amount_3= px.bar(df_3, x = "Transaction_Amount", y = "States", title = "Average Of Transaction Amount", orientation = 'h',
                        color_discrete_sequence= px.colors.sequential.amp_r,width = 1000, height = 800, hover_name = "States")
    st.plotly_chart(fig_amount_3)

# Transaction Count:
def top_chart_transaction_count(table_name):
    # Connection With MySQL :
    mydb = mysql.connector.connect(host = "127.0.0.1",
                                   port = "3306",
                                   user = "root",
                                   password = "Ramya$125",
                                   database = "Phonepe")
    cursor = mydb.cursor(buffered=True)
    
    # Plot 1 :
    
    query1 = f'''select States, sum(transaction_count) as Transaction_Count from {table_name}
                 group by states 
                 order by Transaction_Count desc
                 limit 10;
                    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    
    df_1 = pd.DataFrame(table_1, columns=['States','Transaction_Count'])
    
    col1, col2 = st.columns(2)
    with col1:
        fig_count_1 = px.bar(df_1, x = "States", y = "Transaction_Count", title = " Top 10  =>  Transaction Count",
                                color_discrete_sequence= px.colors.sequential.Peach_r, height = 550,width = 500, hover_name = "States")
        st.plotly_chart(fig_count_1)
    
    # Plot 2:
    
    query2 = f'''select States, sum(transaction_count) as Transaction_Count from {table_name}
                 group by states 
                 order by Transaction_Count 
                 limit 10;
                    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=['States','Transaction_Count'])
    
    with col2 :
        fig_count_2= px.bar(df_2, x = "States", y = "Transaction_Count", title = "Last 10  =>  Transaction Count", width = 600,
                                color_discrete_sequence= px.colors.sequential.Greens_r, height = 615, hover_name = "States")
        st.plotly_chart(fig_count_2)
    
    # Plot 3:
    
    query3 = f'''select States, avg(transaction_count) as Transaction_Count from {table_name}
                 group by states 
                 order by Transaction_Count ;
                    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    
    df_3 = pd.DataFrame(table_3, columns=['States','Transaction_Count'])
    
    fig_count_3= px.bar(df_3, x = "Transaction_Count", y = "States", title = "Average Of Transaction Count", orientation = 'h',
                            color_discrete_sequence= px.colors.sequential.amp_r, height = 800,width = 1000 ,hover_name = "States")
    st.plotly_chart(fig_count_3)

# Map User Register User :

def top_chart_registered_user(table_name, state):
    # Connection With MySQL :
    mydb = mysql.connector.connect(host = "127.0.0.1",
                                   port = "3306",
                                   user = "root",
                                   password = "Ramya$125",
                                   database = "Phonepe")
    cursor = mydb.cursor(buffered=True)
    
    # Plot 1 :
    
    query1 = f'''select Districts, sum(registered_users) as Registered_Users from {table_name}
                 where States = '{state}'
                 group by Districts
                 order by Registered_Users desc
                 limit 10;

                    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    
    df_1 = pd.DataFrame(table_1, columns=['Districts','Registerd_Users'])

    col1, col2 = st.columns(2)
    with col1 :
        fig_amount_1 = px.bar(df_1, x = "Districts", y = "Registerd_Users", title = " Top 10  => Registered Users",width = 600,
                                color_discrete_sequence= px.colors.sequential.YlGnBu_r, height = 615, hover_name = "Districts")
        st.plotly_chart(fig_amount_1)
    
    # Plot 2:
    
    query2 = f'''select Districts, sum(registered_users) as Registered_Users from {table_name}
                 where States = '{state}'
                 group by Districts
                 order by Registered_Users 
                 limit 10;
                    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=['Districts','Registerd_Users'])
    
    with col2 :
        fig_amount_2= px.bar(df_2, x = "Districts", y = "Registerd_Users", title = "Least 10  =>  Registerd Users",height = 615,
                                color_discrete_sequence= px.colors.sequential.Rainbow, width = 600, hover_name = "Districts")
        st.plotly_chart(fig_amount_2)
    
    # Plot 3:
    
    query3 = f'''select Districts, avg(registered_users) as Registered_Users from {table_name}
                 where States = '{state}'
                 group by Districts
                 order by Registered_Users ;
                    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    
    df_3 = pd.DataFrame(table_3, columns=['Districts','Registerd_Users'])
    
    fig_amount_3= px.bar(df_3, x = "Registerd_Users", y = "Districts", title = "Average Of Registerd Users", orientation = 'h',width = 1000,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r, height = 800, hover_name = "Districts")
    st.plotly_chart(fig_amount_3)
        
# Map User App Opens  :

def top_chart_app_opens(table_name, state):
    # Connection With MySQL :
    mydb = mysql.connector.connect(host = "127.0.0.1",
                                   port = "3306",
                                   user = "root",
                                   password = "Ramya$125",
                                   database = "Phonepe")
    cursor = mydb.cursor(buffered=True)
    
    # Plot 1 :
    
    query1 = f'''select Districts, sum(App_Opens) as App_Opens from {table_name}
                where States ='{state}'
                group by Districts
                order by App_Opens desc
                limit 10;

                    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    
    df_1 = pd.DataFrame(table_1, columns=['Districts','App_Opens'])
    
    col1, col2 = st.columns(2)
    with col1 :
        fig_amount_1 = px.bar(df_1, x = "Districts", y = "App_Opens", title = " Top 10  => App Opens",width = 600,
                                color_discrete_sequence= px.colors.sequential.YlGnBu_r, height = 615, hover_name = "Districts")
        st.plotly_chart(fig_amount_1)
    
    # Plot 2:
    
    query2 = f'''select Districts, sum(App_Opens) as App_Opens from {table_name}
                where States ='{state}'
                group by Districts
                order by App_Opens 
                limit 10;
                    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=['Districts','App_Opens'])
    
    with col2 :
        fig_amount_2= px.bar(df_2, x = "Districts", y = "App_Opens", title = "Least 10  =>  App Opens",height = 615,
                                color_discrete_sequence= px.colors.sequential.Rainbow, width = 600, hover_name = "Districts")
        st.plotly_chart(fig_amount_2)
    
    # Plot 3:
    
    query3 = f'''select Districts, avg(App_Opens) as App_Opens from {table_name}
                 where States = '{state}'
                 group by Districts
                 order by App_Opens ;
                    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    
    df_3 = pd.DataFrame(table_3, columns=['Districts','App_Opens'])
    
    fig_amount_3= px.bar(df_3, x = "App_Opens", y = "Districts", title = "Average Of App_Opens", orientation = 'h',width = 1000,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r, height = 800, hover_name = "Districts")
    st.plotly_chart(fig_amount_3)
        
# Top User Register User :

def top_chart_registered_users(table_name):
    # Connection With MySQL :
    mydb = mysql.connector.connect(host = "127.0.0.1",
                                   port = "3306",
                                   user = "root",
                                   password = "Ramya$125",
                                   database = "Phonepe")
    cursor = mydb.cursor(buffered=True)
    
    # Plot 1 :
    
    query1 = f'''select States, sum(registered_users) as Registered_Users from {table_name}
                 group by States
                 order by Registered_Users desc
                 limit 10;

                    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    
    df_1 = pd.DataFrame(table_1, columns=['States','Registerd_Users'])
    
    col1, col2 = st.columns(2)
    with col1 :
        fig_amount_1 = px.bar(df_1, x = "States", y = "Registerd_Users", title = " Top 10  => Registered Users",width = 600,
                                color_discrete_sequence= px.colors.sequential.YlGnBu_r, height = 615, hover_name = "States")
        st.plotly_chart(fig_amount_1)
    
    # Plot 2:
    
    query2 = f'''select States, sum(registered_users) as Registered_Users from {table_name}
                 group by States
                 order by Registered_Users 
                 limit 10;
                    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    
    df_2 = pd.DataFrame(table_2, columns=['States','Registerd_Users'])
    
    with col2 :
        fig_amount_2= px.bar(df_2, x = "States", y = "Registerd_Users", title = "Least 10  =>  Registerd Users",height = 615,
                                color_discrete_sequence= px.colors.sequential.Rainbow, width = 600, hover_name = "States")
        st.plotly_chart(fig_amount_2)
    
    # Plot 3:
    
    query3 = f'''select States, avg(registered_users) as Registered_Users from {table_name}
                 group by States
                 order by Registered_Users ;
                    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    
    df_3 = pd.DataFrame(table_3, columns=['States','Registerd_Users'])
    
    fig_amount_3= px.bar(df_3, x = "Registerd_Users", y = "States", title = "Average Of Registerd Users", orientation = 'h',width = 1000,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r, height = 800, hover_name = "States")
    st.plotly_chart(fig_amount_3)
        



# Streamlit 

st.set_page_config(layout="wide")
st.title(":red[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    select = option_menu("Main Menu",["Home","Data Exploration","Top Charts"],
    icons=['house', 'box','star'], menu_icon="cast", default_index=1)

if select == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("Simple Fast & Secure")
        st.subheader("INDIS's Best Payment App")
        st.write("One app for all things money. Pay Bills, Recharge, Send Money, Buy Gold, Invest and Shop at your favourite stores. ")
    with col2:
            st.video(r"C:\Users\ramya\Phonepe Video.mp4")
    col1, col2 = st.columns(2)
    with col1 :
        st.image(Image.open(r"C:\Users\ramya\Phonepe Image.jpg"))
    with col2 :
        st.subheader("Pay Whenever , Wherever You Like")
        st.write("Choose from options like UPI, the Phonepe Wallet or your Debit and Credit card")
        st.subheader("Find All Your Favourite Apps On Phonepe Switch")
        st.write("Book flights, order food or buy groceries.")
        st.write("Use all your favourite apps without downloading them.")

elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Data","Map Data","Top Data"])

    with tab1 :
        method1 = st.radio("Select One Option To Analysis :",["Aggregated Insurance Data","Aggregated Transaction Data","Aggregated User Data"])

        if method1 == "Aggregated Insurance Data":
            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Aggregated Insuranca Data:",Agg_Insur["Years"].unique())
            agg_insur_tac_Y = tran_amount_count_year(Agg_Insur, years)
            
            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Aggregated Insuranca Data:",agg_insur_tac_Y['Quarters'].unique())
            tran_amount_count_quarter(agg_insur_tac_Y, quarter)
            
        elif method1 == "Aggregated Transaction Data":
            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Aggregated Transaction Data:",Agg_Tran["Years"].unique())
            agg_tran_tac_Y = tran_amount_count_year(Agg_Tran, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select The State To Analysis Aggregated Transaction Data:", agg_tran_tac_Y['States'].unique())
            agg_tran_tran_type(agg_tran_tac_Y,states)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Aggregated Transaction Data:",agg_tran_tac_Y['Quarters'].unique())
            agg_tran_tac_quarter = tran_amount_count_quarter(agg_tran_tac_Y, quarter)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Aggregated Transaction Data:", agg_tran_tac_quarter['States'].unique())
            agg_tran_tran_type(agg_tran_tac_quarter,states)

        elif method1 == "Aggregated User Data":
            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Aggregated User Data:",Agg_User["Years"].unique())
            agg_user_year= agg_user_brand_count_y(Agg_User, years)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Aggregated User Data:",agg_user_year['Quarters'].unique())
            agg_user_quarter = agg_user_brand_count_quarter(agg_user_year, quarter)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select The State To Analysis Aggregated User Data:", agg_user_quarter['States'].unique())
            agg_user_brand_count_state(agg_user_quarter, states)


            

    with tab2 :
        method2 = st.radio("Select One Option To Analysis:",["Map Insurance Data","Map Transaction Data","Map User Data"])

        if method2 == "Map Insurance Data":

            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Map Insurance Data:",Map_Insur["Years"].unique())
            map_insur_tac_Y = tran_amount_count_year(Map_Insur, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select The State To Analysis Map Insurance Data :", map_insur_tac_Y["States"].unique())
            map_insur_dist(map_insur_tac_Y,states)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Map Insurance Data:",map_insur_tac_Y["Quarters"].unique())
            map_insur_tac_quarter = tran_amount_count_quarter(map_insur_tac_Y, quarter)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Map Insurance Data:", map_insur_tac_quarter["States"].unique())
            map_insur_dist(map_insur_tac_quarter,states)


        elif method2 == "Map Transaction Data":
            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Map Transaction Data:",Map_Tran["Years"].unique())
            map_tran_tac_Y = tran_amount_count_year(Map_Tran, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select The State To Analysis Map Transaction Data:", map_tran_tac_Y["States"].unique())
            map_insur_dist(map_tran_tac_Y,states)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Map Transaction Data:",map_tran_tac_Y["Quarters"].unique())
            map_tran_tac_quarter = tran_amount_count_quarter(map_tran_tac_Y, quarter)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Map Transaction Data:", map_tran_tac_quarter["States"].unique())
            map_insur_dist(map_tran_tac_quarter,states)

        elif method2 == "Map User Data":
            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Map User Data:",Map_User["Years"].unique())
            map_user_tac_Y = map_user_year(Map_User, years)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Map User Data:",map_user_tac_Y["Quarters"].unique())
            map_user_tac_quarter = map_user_quarter(map_user_tac_Y, quarter)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Map User Data:", map_user_tac_quarter["States"].unique())
            map_user_state_district(map_user_tac_quarter,states)
            

    with tab3 :
        method3 = st.radio("Select One Option To Analysis:",["Top Insurance Data","Top Transaction Data","Top User Data"])

        if method3 == "Top Insurance Data":

            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select One Year To Analysis Top Insurance Data:",Top_Insur['Years'].unique())
            top_insur_tac_Y = tran_amount_count_year(Top_Insur, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Top Insurance Data:", top_insur_tac_Y["States"].unique())
            top_insur_quarter_state(top_insur_tac_Y,states)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Top Insurance Data:",top_insur_tac_Y["Quarters"].unique())
            top_insur_tac_quarter = tran_amount_count_quarter(top_insur_tac_Y, quarter)           


        elif method3 == "Top Transaction Data":

            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select One Year To Analysis Top Transaction Data:",Top_Tran['Years'].unique())
            top_tran_tac_Y = tran_amount_count_year(Top_Tran, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select One State To Analysis Top Transaction Data:", top_tran_tac_Y["States"].unique())
            top_insur_quarter_state(top_tran_tac_Y,states)

            col1, col2  = st.columns(2)
            with col1 :
                quarter = st.selectbox("Select The Quarter To Analysis Top Transaction Data:",top_tran_tac_Y["Quarters"].unique())
            top_tran_tac_quarter = tran_amount_count_quarter(top_tran_tac_Y, quarter)           


        elif method3 == "Top User Data":

            col1, col2  = st.columns(2)
            with col1 :
                years = st.selectbox("Select The Year To Analysis Top User Data:",Top_User['Years'].unique())
            top_user_Y = top_user_year(Top_User, years)

            col1, col2 = st.columns(2)
            with col1 :
                states = st.selectbox("Select The  State To Analysis Top User Data:", top_user_Y["States"].unique())
            top_user_state(top_user_Y,states)


elif select == "Top Charts":
    question = st.selectbox("Select The Question:", ["1.Transaction Amount and Count Of Aggregated Insurance",
                                                     "2.Transaction Amount and Count Of Map Insurance",
                                                     "3.Transaction Amount and Count Of Top Insurance",
                                                     "4.Transaction Amount and count Of Aggregated Transaction",
                                                     "5.Transaction Amount and count Of Map Transaction",
                                                     "6.Transaction Amount And Count Of Top Transaction",
                                                     "7.Transaction Count Of Aggregated User",
                                                     "8.Registered Users Of Map User",
                                                     "9.App Opens Of Map User",
                                                     "10.Registered Users Of Top user"])

    if question == "1.Transaction Amount and Count Of Aggregated Insurance":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2.Transaction Amount and Count Of Map Insurance":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_insurance")
        
    elif question == "3.Transaction Amount and Count Of Top Insurance":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_insurance")

    elif question == "4.Transaction Amount and count Of Aggregated Transaction":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5.Transaction Amount and count Of Map Transaction":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_transaction")

    elif question == "6.Transaction Amount And Count Of Top Transaction":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_transaction")

    elif question == "7.Transaction Count Of Aggregated User":
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_user")

    elif question == "8.Registered Users Of Map User":

        states = st.selectbox("Select The State  :", Map_User["States"].unique())
        st.subheader("Registered Users")
        top_chart_registered_user("map_user", states)

    elif question == "9.App Opens Of Map User":

        states = st.selectbox("Select One State :", Map_User["States"].unique())
        st.subheader("App Opens")
        top_chart_app_opens("map_user", states)

    elif question == "10.Registered Users Of Top user":

        st.subheader("Registered Users")
        top_chart_registered_users("top_user")
