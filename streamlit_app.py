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
st.subheader("🔔  Analytics Dashboard")
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
"Analyst",
"Business",
"Category",
"IT",
"Question",
"QuestionNo"

FROM Streamlit.dsi.CategoryRatings
"""

# Execute the query and fetch data into a DataFrame
cursor = conn.cursor()
cursor.execute(sql_query)
data = cursor.fetchall()
df = pd.DataFrame(data, columns=[
    'Analyst', 'Business', 'Category', 'IT', 'Question', 'QuestionNo'
])

# Close the cursor and connection
cursor.close()
conn.close()
 


#side bar
st.sidebar.image("logo1.png",caption="Developed and Maintaned by: Rasmus: +4528765537")


#switcher
st.sidebar.header("Please filter")
category=st.sidebar.multiselect(
    "Select Country",
     options=df["Category"].unique(),
     default=df["Category"].unique(),
)


df_selection=df.query(
    "Category==@category"
)








