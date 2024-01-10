import streamlit as st
import csv
import pandas as pd
import hashlib
from time import sleep

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def empty():
    ph.empty()
    sleep(0.01)

st.title('Canoe slalom planner')
if 'username' not in st.session_state: #making a username variable in session ready to store the current users unique username
        st.session_state.username = ''
        
if 'login' not in st.session_state: #if a user hasn't logged in yet then displays the login form
  username_inp = st.text_input('Username')
  hash_object = hashlib.sha1(st.text_input("Password", type="password").encode())
  password_inp = hash_object.hexdigest()
  submit_button = st.button(label='submit')
   
  
  if submit_button:
      #checking passwords correct
      password = ''
      reader = csv.reader(open('username_pass.csv', 'r'))
      for data in reader:
          if data[0] == username_inp:
              password = str(data[1])
              
      if password_inp == password:
          st.session_state.username = username_inp
          st.session_state['login'] = True
          st.success("Login successful")
          st.rerun()
      else:
        st.error('Login failed')
          
if 'login' not in st.session_state: #this means the create an account button will only be made if the user hasn't logged in yet        
    if 'make' not in st.session_state:
        create_button = st.button(label= 'create account', key = 'createbut')
        if create_button:
            st.session_state['make'] = True
    
if 'make' in st.session_state:
    placeholder = st.empty()
    # user can make an account
    with placeholder.container():
             
        new_username = st.text_input("New Username")
        
        col1,col2 = st.columns(2) # seperates names into 2 columns so takes up less space
        
        fname = col1.text_input("First name")
        sname = col2.text_input("Second name")
        hash_object = hashlib.sha1(st.text_input("New password", type = 'password').encode())
        new_password = hash_object.hexdigest()
        athlete_coach = st.selectbox("type",("athlete","coach"))
        
        #different information is required from user depending if they are a coach or athlete
        #displays the correct inputs once the user selects if they are an athelete or coach
        if athlete_coach == "athlete":
            classes_list = st.multiselect("Class",["K1W","C1W","C1M","K1M"])
            division = []
            for item in classes_list:
                division.append( st.selectbox("What is your division for " + item,("prem", "1","2", "3", "4")))
        if athlete_coach == "coach":
            st.write("coach code:")
            
        #saving the details entered by the user into the accounts csv file
        save_butt = st.button("Save")
        data1 = [new_username, fname, sname, athlete_coach]
        data2 = [new_username,new_password]
        filename1 = 'accounts.csv'
        filename2 = 'username_pass.csv'
        if save_butt == True:
            #saving to accounts file
            with open(filename1, 'a') as file:
                for x in data1:
                        file.write(str(x)+',')
                file.write('\n')
            #saving username and hashed passwords to a file
            with open(filename2, 'a') as file:
                for x in data2:
                        file.write(str(x)+',')
                file.write('\n')
            st.session_state.pop('make') #removes the fact create was clicked from session state so that the make an account doesn't appear again
            placeholder.empty()  
            
def CreatePlans_clicked():
          empty()
          with ph.container():
              
              with st.sidebar:
                  name = st.text_input('Enter name of raceplan')
                  uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=False)
                  
def ManageGroups_clicked(): # when user clicks manage groups this function should run and keep running until the user clicks a different main menu option
    ph.empty() 
    with ph.container():
        st.write('manage groups')
                  
def StartList_clicked():  #should display 
    empty()
    with ph.container():
        st.write('start list')
        
def ViewPlans_clicked():
    empty()
    conn = st.connection('mysql', type='sql')

     # Perform query.
    df = conn.query('SELECT * from bibs;', ttl=100)

    with ph.container():
        st.write('view plans')
        for row in df.itertuples():
                st.write(f"{row.bib} has a :{row.paddler}:")        
                  
if 'login' in st.session_state: # if the login is succesful then clear the screen and load home options
    st.empty()
    if 'user_type' not in st.session_state: #creating a user type in session state so that relevant coach/athlete info can be shown
        st.session_state.user_type = ''

    reader = csv.reader(open('accounts.csv', 'r'))
    #finding current user in csv and retrieving if they are an athlete or coach
    for data in reader:
        if data[0] == st.session_state.username:
            st.session_state.user_type = str(data[3]) 
    
    ph = st.empty()
        

    if st.session_state.user_type == "athlete":
      col1,col2 = st.columns(2) #columns to keep buttons at top and in line
      RacePlans_clicked = col1.button("Race plans")
      StartList_clicked = col2.button("Start lists")
      if RacePlans_clicked == True:
              empty()
              with ph.container():
                  st.write('race plans')
     
    
    
    if st.session_state.user_type == "coach":
      col1,col2,col3,col4 = st.columns(4)   #put buttons in columns so that they stay in line at the top of the page
     
      if 'current' not in st.session_state:
          st.session_state.current = None
      
      pages = {
          0 : CreatePlans_clicked,
          1 : ManageGroups_clicked,
          2 : ViewPlans_clicked,
          3 : StartList_clicked,
      }
   
      if col1.button("Create Plans"):
          st.session_state.current = 0
      if col2.button("Manage Groups"):
          st.session_state.current = 1
      if col3.button("View Plans"):
          st.session_state.current = 2
      if col4.button("Start List"):
          st.session_state.current = 3

      if st.session_state.current != None:
          pages[st.session_state.current]()
