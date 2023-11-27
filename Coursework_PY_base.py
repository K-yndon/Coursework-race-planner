
"""
Created on Tue Nov  7 19:53:39 2023

@author: Kate
"""

import streamlit as st   
import pandas as pd 

header = st.container()
inputs = st.container()
with header:
    st.title('Canoe Slalom Planner')

with inputs:
     username = st.text_input('Username','Enter username here')
     password = st.text_input('Password','Enter password here')
     st.markdown('Create account?')

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
                
st.markdown(hide_st_style, unsafe_allow_html=True)
