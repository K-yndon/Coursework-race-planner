import streamlit as st   
import pandas as pd 

# hiding streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """               
st.markdown(hide_st_style, unsafe_allow_html=True)

[theme]
backgroundColor = "#F0F0F0"

#Login page
header = st.container()
inputs = st.container()

with header:
    st.title('Canoe Slalom Planner')

with inputs:
     username = st.text_input('Username','Enter username here')
     password = st.text_input('Password','Enter password here')
     Create_clicked = st.button('Create account?')

