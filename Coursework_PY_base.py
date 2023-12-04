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
            usernames[0]:{
                "name":names[0],
                "password":passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":passwords[1]
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
