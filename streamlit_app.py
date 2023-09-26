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
 


#side bar
st.sidebar.image("logo1.png",caption="Developed and Maintaned by: Rasmus: +4528765537")


#switcher
st.sidebar.header("Please filter")
category=st.sidebar.multiselect(
    "Select Category",
     options=df["Category"].unique(),
     default=df["Category"].unique(),
)


df_selection=df.query(
    "Category==@category"
)



#showData=st.multiselect('Filter: ',df_selection.columns,default=["Analyst","Business","Category","IT","Question","QuestionNo"])
#st.dataframe(df_selection[showData],use_container_width=True)

# Define a color gradient function based on the values
def get_color(val):
    # Choose the color range based on the values
    max_val = max(df['Analyst'].max(), df['IT'].max(), df['Business'].max())
    min_val = min(df['Analyst'].min(), df['IT'].min(), df['Business'].min())
    normalized_val = (val - min_val) / (max_val - min_val)
    return f'background-color: rgb(0, {int(255 - normalized_val * 255)}, 0)'

# Apply the color gradient to the respective columns
styled_df = df_selection.style.applymap(lambda x: get_color(x), subset=['Analyst', 'IT', 'Business'])

# Display the styled DataFrame to fill the entire section
##st.write(styled_df, unsafe_allow_html=True, use_container_width=True)


def Home():
    with st.expander("My Data", expanded=True):
        st.dataframe(styled_df['Question'], use_container_width=True)
Home()

#st.write(styled_df, unsafe_allow_html=True, use_container_width=use_container_width)


