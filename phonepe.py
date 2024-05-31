
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import os
#import psycopg2
import json
import git
import pandas as pd
import mysql.connector
from PIL import Image
import time

#creating dataframe
# Establish connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user2@2024",
    database="phonepe_data",
    port="3306",
    auth_plugin='mysql_native_password'
)

# Create cursor object
c = mydb.cursor()
# Execute the query to fetch data from the 'aggregated_insurance' table
c.execute("SELECT * FROM aggregated_insurance")
# Fetch the results of the query
table1 = c.fetchall()
# Now you can create a DataFrame from the fetched results: # here we could see that column headings are mentioned as 0,1,2,3,4etc. so change the column names we mentioned in this line
Aggre_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount")) #creating df for selected table.

#Aggregated_transsaction
c.execute("select * from aggregated_transaction")
table2 = c.fetchall()
Aggre_transaction = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#Aggregated_user
c.execute("select * from aggregated_user")
table3 = c.fetchall()
Aggre_user = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

c = mydb.cursor()

#Map_insurance
c.execute("select * from map_insurance")
table4 = c.fetchall()
Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))


#Map_transaction
c.execute("select * from map_transaction")
table5 = c.fetchall()
Map_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


#Map_user
c.execute("select * from map_user")
table6 = c.fetchall()
Map_user = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))


#Top_insurance
c.execute("select * from top_insurance")
table7 = c.fetchall()
Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#Top_transaction
c.execute("select * from top_transaction")
table8 = c.fetchall()
Top_transaction = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#Top_user
c.execute("select * from top_user")
table9 = c.fetchall()
Top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

mydb.close()


#function def:

# aggregated insurance: 
# in this we dont have unique transaction_type (i.e) we have only one type so we need not categorize based on it.
def Aggre_insurance_Y(df,year): # to select df we mention 'df', to select 'year' here year is given
    aiy= df[df["Years"] == year] # to select df we mention 'df', to select 'year' here year is given
    aiy.reset_index(drop= True, inplace= True)
    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

#normal bar plot:
# to separate tab page into 2 columns and make each plot display in separate columns under same tab:
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount) # to make chart to get displayed under same tab
    with col2:
        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)  # to make chart to get displayed under same tab


# to display the data in geo visualiztion map form:

    # to separate tab page into 2 columns and make each plot display in separate columns under same tab:
    col1,col2= st.columns(2)

    with col1:
        # to get all info from this url to create map:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson" # this is url map to create map to display states, latitude, longitude,etc.
        response= requests.get(url) #to get response from url and we have imported requested package for this
        data1= json.loads(response.content) # .content = we need content of json file
        #appending state names in states_name_tra = [] list:
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]] #data1["features"] = to access features from data1; feature["properties"]["ST_NM"] = we need only value-names and not key-ST_NM
        states_name_tra.sort() #to sort this list
        
        #creating map from above info:
        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False) #Setting visible=False when creating the map will hide the unwanted geographical features
        
        st.plotly_chart(fig_india_1)
        # in  choropleth, aiyg = df, geojson = data1 (json file), locations= "States" - States from df, featureidkey= "properties.ST_NM" - content of states_name_tra, color= "Transaction_amount" - data to be colored 


    with col2:
        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy
#quarter func of aggregated insurance:
def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq



# def for aggregated transaction:
# we are defining according to "Transaction_type" by passing state as argument and need not consider quarter since we have only one quarter, shown in func:
def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy
def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    auqsg= pd.DataFrame(auqs.groupby("Brands")["Transaction_count"].sum())
    auqsg.reset_index(inplace= True)

    fig_bar_1= px.bar(auqsg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(aguqy, x= "Brands", y= "Transaction_count", hover_data= ["Percentage"],
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#def  for map:
# map function is similar to Aggre_Transaction_type, diff is instead of transaction type we have district here:
#map_insurance and map_transac:
#def map_insure_plot_1(df,state):
def Map_insur_District(df, state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

#map_user:
def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)
    # Reshape the DataFrame to have a row for each combination of state, "RegisteredUsers", and "AppOpens"
    muyg = pd.melt(muyg, id_vars=["States"], value_vars=["RegisteredUser", "AppOpens"], var_name="Metric", value_name="Value")
    fig_map_user_plot_1= px.line(muyg , x= "States", y= "Value", markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)
    # Reshape the DataFrame to have a row for each combination of state, "RegisteredUsers", and "AppOpens"
    muyqg = pd.melt(muyqg, id_vars=["States"], value_vars=["RegisteredUser", "AppOpens"], var_name="Metric", value_name="Value")
    fig_map_user_plot_1= px.line(muyqg, x= "States", y= "Value", markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)



#top:
# top_insurance_plot_1
def Top_insurance_plot_1(df, state): # we need not group here since district are unique values
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= ["Pincodes"],
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= ["Pincodes"],
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.BuGn_r, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUser", hover_data= ["Pincodes"],
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)




#Table creation for query:
#note: all tables have similar name then it should be in similar name format so that we can access multiple tables in each function

def top_chart_transaction_amount(table_name):

    # Establish connection to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="user2@2024",
        database="phonepe_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    c= mydb.cursor()
    # 1st  connection:
    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    c.execute(query1)
    table_1= c.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)



    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
    #above code defaultly goes to ascending
    c.execute(query2)
    table_2= c.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    
    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    c.execute(query3)
    table_3= c.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#2nd sql connection:
def top_chart_transaction_count(table_name):

    # Establish connection to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="user2@2024",
        database="phonepe_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )

    c= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    c.execute(query1)
    table_1= c.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    c.execute(query2)
    table_2= c.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    c.execute(query3)
    table_3= c.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#3rd sql connection:
def top_chart_registered_user(table_name, state):

    # Establish connection to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="user2@2024",
        database="phonepe_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )

    c= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    c.execute(query1)
    table_1= c.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    c.execute(query2)
    table_2= c.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    c.execute(query3)
    table_3= c.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#4th sql connection
def top_chart_appopens(table_name, state):
    # Establish connection to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="user2@2024",
        database="phonepe_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    c= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    c.execute(query1)
    table_1= c.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    c.execute(query2)
    table_2= c.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    c.execute(query3)
    table_3= c.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#5th sql connection
def top_chart_registered_users(table_name):
    # Establish connection to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="user2@2024",
        database="phonepe_data",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    c = mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser DESC
                LIMIT 10;'''

    c.execute(query1)
    table_1= c.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registereduser"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="registereduser", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser
                LIMIT 10;'''

    c.execute(query2)
    table_2= c.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registereduser"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="registereduser", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser;'''

    c.execute(query3)
    table_3= c.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registereduser"))

    fig_amount_3= px.bar(df_3, y="states", x="registereduser", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#Streamlit part

st.set_page_config(layout= "wide")
#title:
st.markdown("<h1 style='color: #6A5ACD; text-align: center;'>PHONEPE DATA VISUALIZATION AND EXPLORATION</h1>", unsafe_allow_html=True)
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])

if select == "Home":
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\imagefront1.png"),width= 1200)
    col1,col2= st.columns(2)

    with col1:
        st.markdown("<h1 style='color: #8A2BE2;'>PHONEPE</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: purple;'>INDIA'S BEST TRANSACTION APP</h3>", unsafe_allow_html=True)
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("***FEATURES***")
        st.markdown("<p style='color: purple;'>*Credit & Debit card linking</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>*Bank Balance check</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>*Money Storage</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>*PIN Authorization</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>*UPI Payments</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>*Bill Payments</p>", unsafe_allow_html=True)

        st.markdown("<style>@keyframes blink {0% {opacity: 1;}50% {opacity: 0;}100% {opacity: 1;}}.blink {animation: blink 1s infinite;}</style><a class='blink' href='https://www.phonepe.com/app-download/'><button style='background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; display: inline-block; font-size: 16px;'>DOWNLOAD THE APP NOW</button></a>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\phonepe1.png"),width= 1000)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\sales-anim.png"),width= 600)

    col3,col4= st.columns(2)

    with col3:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.video("C:\\Users\\lenovo\\Desktop\\try\\phonepe1\\home-fast-secure-v3.mp4")

    with col4:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("<h3 style='color: purple; font-weight: bold;'>Simple, Fast & Secure</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: purple;'>One app for all things money.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: purple;'>Pay whenever you like, wherever you like.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: purple;'>Find all your favourite apps on PhonePe Switch.</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: purple;'>Book flights, order food or buy groceries. Use all your favourite apps without downloading them.</h3>", unsafe_allow_html=True)
    
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
        
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\image2.png"),width= 700)
    st.markdown("<p style='color: purple; text-align: center;'>Payments on PhonePe are safe, reliable and fast. One in three Indians are now using the PhonePe app to send money, recharge, pay bills and do so much more, in just a few simple clicks. PhonePe has also introduced several Insurance products and Investment options that offer every Indian an equal opportunity to unlock the flow of money, and get access to financial services.</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: black; text-align: center;'>#KarteJaBadhteJa</p>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\image3.png"),width= 1200)
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\image4.png"),width= 1200)
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\last1.png"),width= 1200)
    st.image(Image.open(r"C:\Users\lenovo\Desktop\try\phonepe1\last2.png"),width= 1200)
    

if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    
    #AGGREGATED:
    with tab1:
        method = st.radio("**Select the Analysis Method (AGGREGATED)**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        
        #Insurance Analysis:
        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())

            df_agg_insur_Y= Aggre_insurance_Y(Aggre_insurance,years) # use this df for below quarter
            
            col1,col2= st.columns(2) # to separate a page into separate columns i.e. 2 columns
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(), df_agg_insur_Y["Quarter"].min()) # for slider = we have to always give three kind of values like min, max, default

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)
        
        #Transaction Analysis:    
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)

        #User Analysis:
        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",Aggre_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    #MAP:
    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        #Map Insurance Analysis:
        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mi**", Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())

            df_map_insur_Y= Aggre_insurance_Y(Map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            Map_insur_District(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.slider("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
            
            Map_insur_District(df_map_insur_Y_Q, state_m2)

        #Map Transaction Analysis:
        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year_mi**", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            df_map_tran_Y= Aggre_insurance_Y(Map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            Map_insur_District(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            Map_insur_District(df_map_tran_Y_Q, state_m4)
        
        #Map User Analysis:
        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())
 
            df_top_insur_Y= Aggre_insurance_Y(Top_insurance,years_t1)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", df_top_insur_Y["States"].unique())

            Top_insurance_plot_1(df_top_insur_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", Top_transaction["Years"].min(), Top_transaction["Years"].max(),Top_transaction["Years"].min())
 
            df_top_tran_Y= Aggre_insurance_Y(Top_transaction,years_t2)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", df_top_tran_Y["States"].unique())

            Top_insurance_plot_1(df_top_tran_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_tu",Top_user["Years"].min(), Top_user["Years"].max(),Top_user["Years"].min())
            df_top_user_Y= top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", df_top_user_Y["States"].unique())

            top_user_plot_2(df_top_user_Y, states)


elif select == "Top Charts":

    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])
    

    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":

        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":

        states= st.selectbox("Select the State", Map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users("Top_user")
