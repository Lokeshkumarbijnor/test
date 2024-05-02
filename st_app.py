import streamlit as st


st.write("Hi Welcome to my page")
file_name = "abc.txt"
with open(file_name, 'r') as f:
  st.write(f.read())
