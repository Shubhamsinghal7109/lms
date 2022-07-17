import streamlit as st
import firebase_admin
from firebase_admin import db
import pandas as pd
import datetime
@st.cache
def runonce():
    cred=firebase_admin.credentials.Certificate('key.json')
    app=firebase_admin.initialize_app(cred,{"databaseURL":"https://library-fdd93-default-rtdb.firebaseio.com/"})

st.set_page_config(page_title="Library Management System", page_icon="https://cdn-icons-png.flaticon.com/512/212/212807.png")
runonce()
st.sidebar.image("https://www.skoolbeep.com/blog/wp-content/uploads/2020/12/What-is-School-Management-Software-1.png")
st.sidebar.header("Developed by Abhinav Srivastava")
mymenu=st.sidebar.selectbox("MENU",("HOME","ADMIN LOGIN","STUDENT LOGIN"))
st.title("Library Management System")
if(mymenu=="HOME"):
    st.image("https://www.skoolbeep.com/blog/wp-content/uploads/2020/12/WHY-CONSIDER-SKOOLBEEP-THE-BEST-SCHOOL-LIBRARY-AUTOMATION-SOFTWARE-min.png")
elif(mymenu=="ADMIN LOGIN"):
    if 'adminlogin' not in st.session_state:
        st.session_state['adminlogin']=False        
    data=db.reference('/Admin').get()
    with st.form("Login Form"):
        id=st.text_input("Enter Admin ID")
        mypassword=st.text_input('Enter Password')
        loginbutton=st.form_submit_button("LOGIN")
        if loginbutton:
            for i,p in data.items():
                if(i==id and p==mypassword):
                    st.session_state['adminlogin']=True
    if(st.session_state['adminlogin']==True):
        st.subheader("Login Successful")
        choice=st.selectbox("Options",("None","Add New Book","Issued Books"))
        if(choice=="Add New Book"):
            bookname=st.text_input("Enter Book Name")
            bookid=st.text_input("Enter Book ID")
            author=st.text_input("Enter Author Name")
            rowno=st.text_input("Enter any 10 Digit Random Number")
            btn=st.button("ADD BOOK")
            if(btn):
                ref2=db.reference("/Book/"+rowno)
                ref2.update({"Author":author,"Bookid":bookid,"Bookname":bookname})
                st.subheader("Book Added Sucessfully")
        elif(choice=="Issued Books"):
            ref2=db.reference("Issue").get()
            df=pd.DataFrame.from_dict(ref2,orient="index")
            st.dataframe(data=df)
    
elif(mymenu=="STUDENT LOGIN"):
    if 'login' not in st.session_state:
        st.session_state['login']=False
        st.session_state['studentid']=""
    data=db.reference('/Student').get()
    with st.form("Login Form"):
        st.session_state['studentid']=st.text_input("Enter Student ID")
        password=st.text_input('Enter Password')
        loginbutton=st.form_submit_button("LOGIN")
        if loginbutton:
            for i,p in data.items():
                if(i==st.session_state['studentid'] and p==password):
                    st.session_state['login']=True
    if(st.session_state['login']==True):
        st.subheader("Login Successful")
        choice=st.selectbox("Options",("None","Search Book","Issue Book"))
        if(choice=="Search Book"):
            ref2=db.reference("Book").get()
            df=pd.DataFrame.from_dict(ref2,orient="index")
            st.dataframe(data=df) 
        if(choice=="Issue Book"):
            with st.form("Issue book"):
                bookid=st.text_input("Enter book ID")
                date=st.text_input("Enter Date and time upto minutes without any symbol")
                issuebutton=st.form_submit_button("ISSUE BOOK")
                if issuebutton:                     
                     ref3=db.reference("/Issue/"+date)
                     ref3.update({"StudentID":st.session_state['studentid'],"BookID":bookid})
                     st.text("Book Issued Successfully")
                     st.text(datetime.datetime.now())
    
