import streamlit as st   
import pandas as pd 
import streamlit_authenticator as stauth


# hiding streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """               
st.markdown(hide_st_style, unsafe_allow_html=True)

#Login page

names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']

hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {
        "usernames":{
            "jsmith92":{
                "name":"john smith",
                "password":"$2b$12$TSuKwWML0EpbohBQgHx4p8E5q"
                },
            "tturner":{
                "name":"timmy turner",
                "password":"$2b$12$asdaUduuibuEIyBUBHASD896a"
                }            
            }
        }

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
name, authentication_status = authenticator.login('Login','main')

if authentication_status:
    st.write('Welcome *%s*' % (name))
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
