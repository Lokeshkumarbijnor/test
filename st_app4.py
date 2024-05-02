import streamlit as st
import requests
import pandas as pd
import pickle

#df = pd.DataFrame([{"Name": "lokesh"}, {"Name": "easter"}])

st.write("Hi Welcome to my psecond age")
file_url = "https://raw.githubusercontent.com/Lokeshkumarbijnor/test/main/abc.pkl"
res = requests.get(file_url)
res = res.content
df = pd.read_pickle(res)
print(df)
#df.to_pickle('abc.pkl')

st.dataframe(df)
