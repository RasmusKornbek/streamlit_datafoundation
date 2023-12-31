import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")

st.markdown("##")

theme_plotly = None # None or streamlit


#Connect to Snowflake
# Get Snowflake secrets from Streamlit Secrets
snowflake_account = st.secrets["account"]
snowflake_username = st.secrets["username"]
snowflake_password = st.secrets["password"]
snowflake_database = st.secrets["database"]
snowflake_role = st.secrets["role"]
snowflake_schema = st.secrets["schema"]

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=snowflake_account,
    user=snowflake_username,
    password=snowflake_password,
    database=snowflake_database,
    role=snowflake_role,
    schema=snowflake_schema
)

# SQL query
sql_query = """
SELECT 
"CATEGORY",
"QUESTIONNO",
"QUESTION",
"ANALYST",
"BUSINESS",
"IT"



FROM STREAMLIT.DSI.CATEGORYRATINGS
"""

# Execute the query and fetch data into a DataFrame
cursor = conn.cursor()
cursor.execute(sql_query)
data = cursor.fetchall()
df = pd.DataFrame(data, columns=[
    'Category', 'QuestionNo', 'Question', 'Analyst', 'Business', 'IT'
])

# Close the cursor and connection
cursor.close()
conn.close()

#Create empty dataframe
empty = pd.DataFrame()

# Select relevant subset
df_subset = pd.DataFrame(df, columns=[
    'Category', 'Question', 'Analyst', 'Business', 'IT'
])




#side bar
st.sidebar.image("DataFoundation.png",caption="Developed and Maintaned by: Rasmus: +4528765537")
st.sidebar.header("Select relevant context")


option_select = st.sidebar.radio(
    'Select stakeholder:',
    options=['Business', 'IT', 'Analyst']
)


#switcher
category=st.sidebar.multiselect(
    "Select Category",
     options=df_subset["Category"].unique(),
     default=df_subset["Category"].unique(),
)




df_selection=df_subset.query(
    "Category==@category"
)


df_dynamic_columns = df_selection[["Category", "Question", option_select]]
df_dynamic_columns_sorted = df_dynamic_columns.sort_values(by=[option_select])


# Define a color gradient function based on the values
def get_color(val):
    # Choose the color range based on the values
    max_val = max(df['Analyst'].max(), df['IT'].max(), df['Business'].max())
    min_val = min(df['Analyst'].min(), df['IT'].min(), df['Business'].min())
    normalized_val = (val - min_val) / (max_val - min_val)
    return f'background-color: rgb(0, {int(255 - normalized_val * 255)}, 0)'

# Apply the color gradient to the respective columns
styled_df = df_dynamic_columns_sorted.style.applymap(lambda x: get_color(x), subset=[option_select])

# Display the styled DataFrame to fill the entire section
##st.write(styled_df, unsafe_allow_html=True, use_container_width=True)


st.subheader("Sales Questionaire - Data Foundation")
def Home():
    with st.expander("", expanded=True):
        st.dataframe(styled_df, use_container_width=True, height=900)
Home()

#st.write(styled_df, unsafe_allow_html=True, use_container_width=use_container_width)


