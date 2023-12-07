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

Create_clicked = st.button('Create account?')
Guest_clicked = st.button('Continue as guest')
Login_clicked = st.button('Login')

def Create_account():
  F_name_new = st.text_input('First name')
  S_name_new = st.text_input('Second name')
  Username_new = st.text_input('Username')
  Coach_state_new = st.selectbox('Are you primarily a coach or athlete?', ('Athlete', 'Coach'))

if Login_clicked == True:
  check_password()
if Create_clicked == True:
  Create_account()

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

    # Setting layout and inputs
    st.title('Canoe Slalom Planner')
    Username = st.text_input('Username')
    st.text_input("Password", type="password", on_change=password_entered, key="password")
   
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.





#Home page
st.title("Canoe slalom Planner")
def User_athlete():
  st.write("athlete home")
  RacePlans_clicked = st.button("Race plans")
  StartList_clicked = st.button("Start lists")
def User_coach():
  st.write("coach home")
  ViewPlans_clicked = st.button("View Plans")
  CreatePlans_clicked = st.button("Create Plans")
  StartList_clicked = st.button("Start Lists")
  ManageGroups_clicked = st.button("Manage Groups")

user_type = "coach"
if user_type == "athlete":
  User_athlete()

if user_type == "coach":
  User_coach()
  
  


