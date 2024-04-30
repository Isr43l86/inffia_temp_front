import streamlit as st
from dotenv import load_dotenv

from menu import menu
from models.userModel import UserModel
from pages.login.components import loginFormComponent, signUpComponent, verifyEmailComponent

load_dotenv()

if 'current_user' not in st.session_state:
    st.session_state.current_user = UserModel(userId=None, accountId=None, conversationId=None, accessToken=None)

if 'current_form' not in st.session_state:
    st.session_state.current_form = 'signin'

if st.session_state.current_form == 'signin':
    loginFormComponent.login_form()

if st.session_state.current_form == 'signup':
    signUpComponent.sign_up_component()

if st.session_state.current_form == 'verification_code':
    verifyEmailComponent.verify_email_component()

menu()
