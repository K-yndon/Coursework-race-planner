import streamlit as st
import csv
import pandas as pd
import hashlib
from time import sleep
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=st.secrets['db']["db_pass"],
  database="race_db"
)

mycursor = mydb.cursor()


hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#-------------------------------------------------------------------------------------------------------
#functions for login

     
def logout():
    logout = st.button('logout')
    if logout:
        for key in st.session_state.keys(): #goes through and deletes all the session state variables, including the logged in status
            del st.session_state[key]

def check_userpass(INPusername,INPpassword):
    mycursor.execute("SELECT Username, Passwords FROM users") 
    myresult = mycursor.fetchall()
    
    password = ''
    for x in myresult:
      if x[0] == INPusername:
          password = str(x[1])
    if password == INPpassword:
        st.session_state.username = INPusername
        st.session_state['login'] = True
        st.experimental_rerun()
    else:
      st.error('Login failed')
    
                
def login():
    if 'login' not in st.session_state: #if a user hasn't logged in yet then displays the login form
      username_inp = st.text_input('Username')
      hash_object = hashlib.sha1(st.text_input("Password", type="password").encode())
      password_inp = hash_object.hexdigest() #hashing the input to see if it matches hashed value in database
      submit_button = st.button(label='submit')
      
      if 'username' not in st.session_state: #making a username variable in session ready to store the current users unique username
        st.session_state.username = '' 
      
      if submit_button:
          check_userpass(username_inp,password_inp)
          
#------------------------------------------------------------------------------------------------------------------------
#functions for sign up

def formatt_classes(classlist,divisionlist):
    newlist = []
    for i in range(0,len(classlist)):
        if divisionlist[i] == 'prem':
            if classlist[i] == 'K1W':
                newlist.append('W')
            elif classlist[i] == 'K1M':
                newlist.append('M')
            else:
                newlist.append(classlist[i])
        else:
            if classlist[i] == 'K1W':
                newlist.append(str(divisionlist[i]) + 'W')
            elif classlist[i] == 'K1M':
                newlist.append(str(divisionlist[i]) + 'M')
            else:
                newlist.append(str(divisionlist[i]) + classlist[i])
    return newlist
  
def make_account():
    if 'login' not in st.session_state: #this means the create an account button will only be made if the user hasn't logged in yet        
        if 'make' not in st.session_state:
            create_button = st.button(label= 'create account', key = 'createbut')
            if create_button:
                st.session_state['make'] = True
        
    if 'make' in st.session_state: #Form for making a new account and then saving the data to a csv
        placeholder = st.empty()
        # user can make an account
        with placeholder.container(): # allows the form to be cleared when a user logs in
                 
            new_username = st.text_input("New Username")
            
            col1,col2 = st.columns(2) # seperates names into 2 columns so takes up less space
            
            fname = col1.text_input("First name").capitalize()
            sname = col2.text_input("Second name").upper()
            hash_object = hashlib.sha1(st.text_input("New password", type = 'password').encode())
            new_password = hash_object.hexdigest()
            athlete_coach = st.selectbox("type",("athlete","coach"))
            
            #different information is required from user depending if they are a coach or athlete
            #displays the correct inputs once the user selects if they are an athelete or coach
            if athlete_coach == 'athlete':
                temp_list = st.multiselect("Class",["K1W","C1W","C1M","K1M"])
                division_list = []
                bib_list = []
                for item in temp_list:
                    division_list.append( st.selectbox("What is your division for " + item,("prem", "1","2", "3", "4")))
                    bib_list.append(st.number_input("What is your bib for " + item, value=5, min_value = 1, max_value = 300,step =1))
                    
                classes_list = formatt_classes(temp_list,division_list)  #to store classes in same format as start lists
            #saving the details entered by the user into the accounts csv file
            save_butt = st.button("Save")
            val1 = [new_username, new_password, fname, sname,athlete_coach]
            
            
            if save_butt:
                sql = "INSERT INTO users () VALUES (%s, %s,%s,%s,%s)"  #%s is used to prevent against sql injection attacks
                mycursor.execute(sql, val1)
                mydb.commit()
                if athlete_coach == 'athlete':
                    val2 = [bib_list[0],new_username,classes_list[0],division_list[0]]
                    sql = "INSERT INTO bibs (Bib,Username,Category,Division) VALUES (%s, %s,%s,%s)"
                    mycursor.execute(sql, val2)
                    mydb.commit()
                    if len(classes_list) == 2:
                        val3 = [bib_list[1],new_username,classes_list[1],division_list[1]]
                        sql = "INSERT INTO bibs (Bib,Username,Category,Division) VALUES (%s, %s,%s,%s)"
                        mycursor.execute(sql, val3)
                        mydb.commit()
                
                st.session_state.pop('make') #removes the fact create was clicked from session state so that the make an account doesn't appear again
                placeholder.empty()  
                
                
def empty():
    ph.empty()
    sleep(0.01)
      
#----------------------------------------------------------------------------------------------------------------------------           
# Functions for creating plan

def find_athlete(fname,sname,startlist):
    column_names = ['bib', 'class', 'fname','sname',' f','','age','club','practice','first run','second run','official']
    df= pd.read_csv(startlist, names=column_names) #adds names to columns of startlist
    data = df.loc[(df['fname'] ==  fname) & (df['sname'] == sname)] #searches database for both fname and sname columns
    
    if data.empty or (len(data) > 2):
        return False, data.reset_index(drop=True)  #returns it without index
    elif len(data) == 2:
        return 'multiple', data.reset_index(drop=True)
    else:
        return True, data.reset_index(drop=True)
    
    
def reformatt_row(data):
    new_row = {
               'Class' : data['class'][0],
               'Bib' : data['bib'][0],
               'F Name' : data['fname'][0], 
               'S Name' : data['sname'][0],
               'Course walk': ' ',  #editable table doesn't allow characters if left empty
               'Run 1': data['first run'][0],
               'Video review': ' ',
               'Run 2': data['second run'][0]
               }    
    return new_row

def get_bibID(username,row):
         val = [username, row['Class'][0]]
         sql = "SELECT BibID FROM bibs WHERE Username = %s AND Category = %s"
         st.write('values searching for in db')
         val
         mycursor.execute(sql,val) #finding the BibID from the username 
         BibID = mycursor.fetchall()
         return BibID
         
def save_plan(df,notes,raceID, rpName, division):  #for saving coaches plan to mysql database
     
     for i in range(0,len(df)): #for each row in the coaches plan checking data and then saving in plan table
         #selecting just the current row from the database to keep track easier, its not necessary to the function of the loop
         temp = df.loc[i:, ['Class','Bib', 'F Name', 'S Name', 'Course walk','Run 1', 'Video review','Run 2']] 
         row = temp.reset_index(drop=True) #row would keep original index from the df otherwise 
         sql = "SELECT username FROM users WHERE Fname = %s AND Sname = %s AND coaches = 'athlete'" #only want to select athletes as need associated bibID, coaches dont have bibID
         val1 = (row['F Name'][0],row['S Name'][0]) #column name then index, index will always be zero as loops through
         mycursor.execute(sql, val1)
         temp = mycursor.fetchall()
                 
         if len(temp) > 0: #if there is a user with the correct name then get the bibID
             username = temp[0][0]
             st.write('user exists username is ' + username)
             
         else:  #if the name doesnt exist then add it to the users table
             username = row['F Name'][0] + row['S Name'][0]
             st.write('user doesnt exist, username is '+username)
             sql = "INSERT INTO users(fname,sname,username,coaches) VALUES (%s, %s,%s,%s)"
             val1 = [row['F Name'][0],row['S Name'][0], username, 'athlete']
             st.write('values being inserted into users ')
             val1
             mycursor.execute(sql, val1) #inserting new user to store name
             mydb.commit()
 
         BibID = get_bibID(username,row) #get the bib id
         
         # the username can exist whilst only having 1 bib of 2 registered,
         if len(BibID) == 0:  #if the bib doesn't exist add it to the bib table linked to the user
             sql2 = "INSERT INTO bibs(Bib,Username,Category,Division) VALUES (%s, %s,%s,%s)"
             val2 = [int(row['Bib'][0]),username, row['Class'][0], division]  
             st.write('values being inserted into bibs ')
             val2
             mycursor.execute(sql2, val2)  #inserting new bib info to link to plan
             mydb.commit()
         
             BibID = get_bibID(username,row) #get the new bib id if added as it autoincriments
         
         st.write('bib id value')
         BibID
         
         #inserting row with associated foreign keys into plan table
         sql3 = "INSERT INTO plan(BibID, RaceID, Coach, PlanName,Practice,Run1,Run2,Coursewalk,Video,Notes) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
         val3 = [BibID[0][0],raceID,st.session_state.username,rpName,'',row['Run 1'][0], row['Run 2'][0], row['Course walk'][0], row['Video review'][0],notes]
         st.write(val3)
         mycursor.execute(sql3, val3)  #inserting each row into the mysql database
         mydb.commit()
     
            
def CreatePlans_clicked(): #coach
          empty()
          if 'plan_df' not in st.session_state: #needs to be in session state otherwise will reset df to nothing
             st.session_state.plan_df = pd.DataFrame(columns=['Class','Bib', 'F Name', 'S Name', 'Course walk','Run 1', 'Video review','Run 2'])
          
          with ph.container():
              
              new_row = {}
              with st.sidebar:
                  mycursor.execute("SELECT RaceID,NameRace,DateRace FROM races")                 
                  myresult = [['','','']]#creates blank in select box so can see if user has selected race or uploaded one
                  
                  for item in mycursor.fetchall():
                      myresult.append(item)#adding races to list so that they can be selected
                      
                  #user selecting which race that times will be extracted from for the plan
                  with st.expander('Race'): #takes up a lot of room so can collapse race selection once decided
                      choose_race = st.selectbox("Choose race", [(str(opt[0])+' ' +str(opt[1]) + ' ' + str(opt[2])) for opt in myresult]) #displaying available races
                      st.write('Or upload start list')
                      uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=False)
                      
                  if choose_race != '  ': # if the user selects a race stored locally
                      placeholder = choose_race.split() #splitting up user choice
                      current_raceID = int(placeholder[0])
                      val = [current_raceID] #getting the race ID that the user selected
                      sql = "SELECT file_name FROM races WHERE raceID = %s"
                      mycursor.execute(sql,val)
                      startlist = (mycursor.fetchall()[0][0])
                      
                  elif uploaded_files != '': #if the user decides to user an uploaded start list
                      startlist = uploaded_files
                      current_raceID = 'null'
                     
                      
                  rp_name = st.text_input('Enter name of raceplan')
                  division =  st.selectbox("Division of race",("prem", "1","2", "3", "4"))
                  
                  #adding athlete to raceplan
                  with st.expander('Add paddler to plan'):
                      col1,col2 = st.columns(2)
                      fname = (col1.text_input('First name')).capitalize()
                      sname = (col2.text_input('Second name')).upper()
                      
                      #process of searching start list for coaches input and displaying to user
                      if col2.button('Add'):
                          result = find_athlete(fname,sname,startlist) #find out if athlete in start list and returns their info 
                          found = result[0] #first returned item indicates whether athlete exists/if they have multiple classes
                          athlete_data = result[1] #second item is a dataframe containing the athletes times
                          if found == False:
                             st.write('No user data found / duplicate names in start list')
                             
                          elif found == 'multiple':  #for athlete with multiple disciplines so multiple run times
                              for i in range(0,len(athlete_data)):
                                  data = athlete_data.loc[i:, ['bib', 'class', 'fname','sname',' f','','age','club','practice','first run','second run','official']]
                                  new_row = reformatt_row(data.reset_index(drop=True)) #resets index otherwise first entry keeps its original index
                                  st.session_state.plan_df.loc[len(st.session_state.plan_df)] = new_row  #adds each row to the dataframe displayed to user
                                  
                          else: #if athlete being added has just 1 discipline
                              new_row = reformatt_row(athlete_data)
                              st.session_state.plan_df.loc[len(st.session_state.plan_df)] = new_row #adds athlete data to session state dataframe
                              
                  Notes = st.text_area('Notes for plan', height=175)  #additional notes that user wants to add to plan
              
              #not in sidebar but in place holder to be cleared
              annotated_df = st.data_editor(st.session_state.plan_df, hide_index=True, use_container_width=True, disabled=["Class", "Bib","Name"])            
              
              if st.button('Save'):
                  save_plan(annotated_df,Notes, current_raceID, rp_name, division)
                  st.success('Saved plan!')
 
#-----------------------------------------------------------------------------------------------------------------------------

def ManageGroups_clicked(): # coach, when user clicks manage groups this function should run and keep running until the user clicks a different main menu option
    ph.empty() 
    with ph.container():
        st.write('manage groups')
        
#--------------------------------------------------------------------------------------------------------------
                  
def StartList_clicked():  #coach
    empty()
    with ph.container():
        st.write('start list')
        with st.sidebar:
            st.write('Select start list')
            
#----------------------------------------------------------------------------------------------------------------
            
def ViewPlans_coach(): #coach, different info shown compared to athlete
    empty()
    

    with ph.container():
        st.write('view plans')
        with st.sidebar:
            st.write('Select plan')
#-------------------------------------------------------------------------------------------------------------------
def display_individual(times,bib):
    st.write('Class: ' + bib[1])
    st.write('Practice: ' + str(times[0][2]))
    st.write('Coursewalk: ' + str(times[0][3]))
    st.write('First run: '+ str(times[0][4]))
    st.write('Video review: '+ str(times[0][5]))
    st.write('Second run: '+ str(times[0][6]))
    st.write('')
    st.write('Coach is: ' + times[0][1])
    st.write('---------------------------------------------')
        
def reformat_row_view(data):
    val = [data[0]]
    sql = "SELECT Bib,Username, Category FROM bibs WHERE BibID = %s"
    mycursor.execute(sql,val)
    bibs = mycursor.fetchall()
    
    val = [bibs[0][1]]
    sql = "SELECT Fname,SName FROM users WHERE Username = %s"
    mycursor.execute(sql,val)
    users = mycursor.fetchall()
    
    
    new_row = {
               'Class' : bibs[0][2],
               'Bib' : bibs[0][0],
               'F Name' : users[0][0], 
               'S Name' : users[0][1],
               'Practice': str(data[2]),
               'Course walk': str(data[3]),
               'Run 1': str(data[4]),
               'Video review': str(data[5]),
               'Run 2': str(data[6])
               }    
    return new_row   
   
def display_whole(plan):
   
    if 'Aplan_df' not in st.session_state: #needs to be in session state otherwise will reset df to nothing, athlete version
       st.session_state.Aplan_df = pd.DataFrame(columns=['Class','Bib', 'F Name', 'S Name', 'Practice','Course walk','Run 1', 'Video review','Run 2'])
    
    for i in range(0,len(plan)):
        new_row = reformat_row_view(plan[i])
        st.session_state.Aplan_df.loc[len(st.session_state.Aplan_df)] = new_row  #adding new row to table showed to user
        
    st.dataframe(st.session_state.Aplan_df,hide_index = True)
    
    if plan[0][7] is not None:  #can't concatenate if notes variable is empty
        st.write('Notes: ' + plan[0][7]) # notes should be same from same plan
               
        

def RacePlans_athlete():  #athlete, athlete needs individual view as well
    empty()
    with ph.container():
        st.write('race plans')
        val = [st.session_state.username]
        sql = "SELECT BibID, Category FROM bibs WHERE username = %s"  #collecting the relevant bib info of current user 
        mycursor.execute(sql,val)
        user_BibID = mycursor.fetchall()
      
        #finding out what raceID's link to the current athlete user by their bibID
        val = [user_BibID[0][0]]
        sql = "SELECT RaceID FROM plan WHERE BibID = %s" 
        mycursor.execute(sql,val) 
        race_ids = mycursor.fetchall()   
        
    
        with st.sidebar:
            races = []
            for item in race_ids:
                sql = "SELECT RaceID,PlanName FROM plan WHERE RaceID = %s"
                val = [race_ids[0][0]]
                mycursor.execute(sql,val)
                res = mycursor.fetchall()
                races.append(res[0])
                
            if races[0] != '':
                temp = st.selectbox("Select plan", [(str(opt[0])+'-' +str(opt[1])) for opt in races])
                chosen_plan = temp.split('-')
                display = True
            else:
                st.write('You have no plans assigned to your user yet')
                
            howToView = st.selectbox('How do you want to see the plan?',('individual','Whole plan'))    
            
        if display:  #need to display plan outside of the sidebar so needs to be in seperate if statement
           if howToView == 'Whole plan':
              sql = "SELECT BibID,Coach,Practice,Coursewalk,Run1,Video,Run2,Notes FROM plan WHERE RaceID = %s AND PlanName = %s"
              val = [chosen_plan[0],chosen_plan[1]]
              mycursor.execute(sql,val)
              whole_plan = mycursor.fetchall()
              display_whole(whole_plan)
              
           else:
               col1,col2 = st.columns(2)
               for i in range(0,len(user_BibID)):
                   sql = "SELECT BibID,Coach,Practice,Coursewalk,Run1,Video,Run2,Notes FROM plan WHERE RaceID = %s AND PlanName = %s AND BibID = %s"
                   val = [chosen_plan[0],chosen_plan[1],user_BibID[i][0]]
                   mycursor.execute(sql,val)
                   res = mycursor.fetchall()
                   
                   with col1:
                       display_individual(res,user_BibID[i])
               with col2:
                    if res[0][7] is not None:  #can't concatenate if notes variable is empty
                        st.write('Notes: ' + res[0][7]) # notes should be same from same plan
           
           
#------------------------------------------------------------------------------------------------------------------------


coll1,coll2 = st.columns([7,1])
coll1.title('Canoe slalom planner')
with coll2:
    logout()      
login()        
make_account()     

             
if 'login' in st.session_state: # if the login is succesful then clear the screen and load home options
    st.empty()
                              
    if 'user_type' not in st.session_state: #creating a user type in session state so that relevant coach/athlete info can be shown
        st.session_state.user_type = ''

    #find out if user is coach or athlete
    sql = "SELECT coaches FROM users WHERE username = %s"
    val1 = (st.session_state.username,)
    mycursor.execute(sql, val1)
    myresult = mycursor.fetchall()
    st.session_state.user_type = myresult[0][0]
    
    ph = st.empty()
        
#------------------------------------------------------------------------------------------------
    if st.session_state.user_type == "athlete":
      col1,col2 = st.columns(2) #columns to keep buttons at top and in line
      
      if 'current' not in st.session_state: #this is a placeholder for what button is currently in use and so what needs to be displayed
          st.session_state.current = None
      
      pages = { #rather than writing out each function name 
          0 : RacePlans_athlete,
          1 : StartList_clicked,
      }
   
      if col1.button("Race Plans"):
          st.session_state.current = 0
      if col2.button("Start List"):
          st.session_state.current = 1

      if st.session_state.current != None: #when current session state is set to a value, the function related to the page number is called e.g.create plans
          pages[st.session_state.current]()

#----------------------------------------------------------------------------------------------------------------------           
    if st.session_state.user_type == "coach":
      col1,col2,col3,col4 = st.columns(4)   #put buttons in columns so that they stay in line on the page at all times
     
      if 'current' not in st.session_state: #this is a placeholder for what button is currently in use and so what needs to be displayed
          st.session_state.current = None
      
      pages = { #rather than writing out each function name 
          0 : CreatePlans_clicked,
          1 : ManageGroups_clicked,
          2 : ViewPlans_coach,
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

      if st.session_state.current != None: #when current session state is set to a value, the function related to the page number is called e.g.create plans
          pages[st.session_state.current]()
