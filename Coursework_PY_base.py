
"""
Created on Tue Nov  7 19:53:39 2023

@author: Kate
"""

import streamlit as st   
import pandas as pd 

header = st.container()

with header:
    st.title('Welcome to my project')



hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
                
st.markdown(hide_st_style, unsafe_allow_html=True)