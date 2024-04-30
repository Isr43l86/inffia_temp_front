import os

import requests
import streamlit as st


def login_form():
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
                st.session_state.current_user.accountId = response['account']['account_id']
                st.session_state.current_user.accessToken = response['access_token']['access_token']
            except Exception as e:
                st.exception(e)

        if btn_goto_signup:
            st.session_state.current_form = 'signup'
            st.rerun()


if __name__ == "__main__":
    login_form()
