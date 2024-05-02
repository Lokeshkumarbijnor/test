import streamlit as st


st.write("Hi Welcome to my psecond age")
file_name = "https://raw.githubusercontent.com/Lokeshkumarbijnor/test/main/abc.txt"
st.write(file_name)
print(file_name)
with open(file_name, 'r') as f:
  
  st.write(f.read())
