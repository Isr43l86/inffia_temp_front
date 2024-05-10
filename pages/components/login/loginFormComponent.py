import os

import requests
import streamlit as st

from errorConstants import LOGIN_EMPTY_EMAIL, LOGIN_EMPTY_PASSWORD


def login_form():
    with st.form('Login', clear_on_submit=True):
        st.header('Login')
        user_login_email = st.text_input('Correo electrónico:', placeholder='Ingresa tu correo electrónico')
        user_login_password = st.text_input('Contraseña', type='password', placeholder="Ingresa tu contraseña")
        btn_login = st.form_submit_button('Iniciar sesión', use_container_width=True, type='primary')
        btn_goto_signup = st.form_submit_button('Registrate', use_container_width=True, type='secondary')

        if btn_login:

            if not user_login_email:
                st.error(LOGIN_EMPTY_EMAIL, icon="🚨")
                st.stop()
            if not user_login_password:
                st.error(LOGIN_EMPTY_PASSWORD, icon="🚨")
                st.stop()

            try:
                response = requests.post(f'{os.getenv("BASE_URL")}/inffia/api/v1/users/login', json={
                    'email': user_login_email,
                    'password': user_login_password,
                })

                response_json = response.json()

                if response.status_code != 201:
                    st.error(response_json['detail'], icon="🚨")
                else:
                    st.session_state.current_user.userId = response_json['user_id']
                    st.session_state.current_user.accountId = response_json['account']['account_id']
                    st.session_state.current_user.accessToken = response_json['access_token']['access_token']
                    st.switch_page("pages/llmCoip.py")

            except Exception as e:
                st.exception(e)

        if btn_goto_signup:
            st.session_state.current_form = 'signup'
            st.rerun()


if __name__ == "__main__":
    login_form()
