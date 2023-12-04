import streamlit as st   
import pandas as pd 
import hmac

# hiding streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """               
st.markdown(hide_st_style, unsafe_allow_html=True)

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    username = st.text_input('Username','Enter username here')
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.


#Login page
header = st.container()
inputs = st.container()

with header:
    st.title('Canoe Slalom Planner')

with inputs:
     username = st.text_input('Username','Enter username here')
     password = st.text_input('Password','Enter password here')
     Create_clicked = st.button('Create account?')

