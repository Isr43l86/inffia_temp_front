import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

from appConstants import MESSAGES_SIGNUP_SUCCESS, MESSAGES_EMAIL_VERIFIED_SUCCESS
from dependencies import verify_email
from errorConstants import SIGNUP_EMAIL_INVALID, SIGNUP_PHONE_INVALID, SIGNUP_NOT_SAME_PASSWORD
from menu import menu
from models.userModel import UserModel

load_dotenv()

if 'current_user' not in st.session_state:
    st.session_state.current_user = UserModel(userId=None, accountId=None, conversationId=None, accessToken=None)

if 'current_form' not in st.session_state:
    st.session_state.current_form = 'signin'

if st.session_state.current_form == 'signin':
    with st.form('Login', clear_on_submit=True):
        st.header('Login')
        user_login_email = st.text_input('Correo electrónico:', placeholder='Ingresa tu correo electrónico')
        user_login_password = st.text_input('Contraseña', type='password', placeholder="Ingresa tu contraseña")
        btn_login = st.form_submit_button('Iniciar sesión', use_container_width=True, type='primary')
        btn_goto_signup = st.form_submit_button('Registrate', use_container_width=True, type='secondary')

        if btn_login:
            try:
                response = requests.post(f'{os.getenv("BASE_URL")}/inffia/api/v1/users/login', json={
                    'email': user_login_email,
                    'password': user_login_password,
                })
                response = response.json()
                st.write(response)
                st.session_state.current_user.userId = response['user_id']
                st.session_state.current_user.accountId = response['user_account']['account_id']
                st.session_state.current_user.accessToken = response['access_token']['access_token']
            except Exception as e:
                st.exception(e)

        if btn_goto_signup:
            st.session_state.current_form = 'signup'
            st.rerun()

if st.session_state.current_form == 'signup':
    with st.form("Signup", clear_on_submit=True):
        st.header('Registrate')
        user_signup_name = st.text_input('Nombre', placeholder='Ingresa tu nombre')
        user_signup_lastname = st.text_input('Apellido', placeholder='Ingresa tu apellido')
        user_signup_email = st.text_input('Correo electrónico', placeholder='Ingresa tu correo electrónico')
        if not verify_email(user_signup_email) and user_signup_email:
            st.error(SIGNUP_EMAIL_INVALID)

        col1, col2 = st.columns([2.3, 10])
        with col1:
            st.selectbox('Teléfono', ['🇪🇨  (+593)'])
        with col2:
            user_signup_phone = st.text_input('Teléfono', max_chars=9, placeholder='Ingresa tu número de teléfono',
                                              label_visibility='hidden')
        if (user_signup_phone.isalpha() or len(user_signup_phone) < 9) and user_signup_phone:
            st.error(SIGNUP_PHONE_INVALID)

        user_signup_password = st.text_input('Contraseña', type='password', placeholder="Ingresa tu contraseña")
        user_signup_password_verify = st.text_input('Repite tu contraseña', type='password', placeholder="Repite tu "
                                                                                                         "contraseña")

        if user_signup_password != user_signup_password_verify and user_signup_password_verify:
            st.error(SIGNUP_NOT_SAME_PASSWORD)

        btn_signup = st.form_submit_button('Crear cuenta', use_container_width=True, type='primary')
        btn_goto_login = st.form_submit_button('Inicia sesión', use_container_width=True, type='secondary')

        if btn_signup:
            try:
                response = requests.post(f'{os.getenv("BASE_URL")}/inffia/api/v1/users/signup', json={
                    'email': user_signup_email,
                    'password': user_signup_password,
                    'phone': f"593{user_signup_phone}",
                    'first_name': user_signup_name,
                    'lastname': user_signup_lastname,
                })
                response = response.json()
                st.write(response)
                st.session_state.current_user.userId = response['user_id']
                st.session_state.current_user.accountId = response['account']['account_id']
                st.success(MESSAGES_SIGNUP_SUCCESS, icon="✅")
                st.session_state.current_form = 'verification_code'
                time.sleep(3)
                st.rerun()
            except Exception as e:
                st.exception(e)

        if btn_goto_login:
            st.session_state.current_form = 'signin'
            st.rerun()

if st.session_state.current_form == 'verification_code':
    with st.form('Login', clear_on_submit=True):
        st.header('Verifica tu cuenta')
        st.markdown('Ingresa el código de verificación que ha sido enviado a tu correo')
        user_verification_code = st.text_input("Código de verificación",
                                               placeholder="Ingresa el código de verificación que recibiste")
        btn_verify_account = st.form_submit_button('Verificar cuenta', use_container_width=True, type='primary')
        if btn_verify_account:
            try:
                requests.post(
                    f'{os.getenv("BASE_URL")}/inffia/api/v1/accounts/verification/'
                    f'{st.session_state.current_user.accountId}/{user_verification_code}'
                )
                st.session_state.current_user.accessToken = response['access_token']
                st.success(MESSAGES_EMAIL_VERIFIED_SUCCESS, icon="✅")
            except Exception as e:
                st.exception(e)

menu()
