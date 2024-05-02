import streamlit as st


st.write("Hi Welcome to my page")
file_name = "https://github.com/Lokeshkumarbijnor/test/blob/main/abc.txt"
print(file_name)
with open(file_name, 'r') as f:
  
  st.write(f.read())
