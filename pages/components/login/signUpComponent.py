import os

import requests
import streamlit as st

from dependencies import verify_email
from errorConstants import (
    SIGNUP_EMAIL_INVALID,
    SIGNUP_PHONE_INVALID,
    SIGNUP_NOT_SAME_PASSWORD,
    SIGNUP_EMPTY_NAME,
    SIGNUP_EMPTY_LASTNAME,
    SIGNUP_EMPTY_EMAIL,
    SIGNUP_EMPTY_PHONE,
    SIGNUP_EMPTY_PASSWORD,
)


def sign_up_component():
    with st.form("Signup", clear_on_submit=True):
        st.header('Registrate')
        user_signup_name = st.text_input('Nombre', placeholder='Ingresa tu nombre')
        user_signup_lastname = st.text_input('Apellido', placeholder='Ingresa tu apellido')
        user_signup_email = st.text_input('Correo electrónico', placeholder='Ingresa tu correo electrónico')
        if not verify_email(user_signup_email) and user_signup_email:
            st.error(SIGNUP_EMAIL_INVALID, icon="🚨")

        col1, col2 = st.columns([2.3, 10])
        with col1:
            st.selectbox('Teléfono', ['🇪🇨  (+593)'])
        with col2:
            user_signup_phone = st.text_input('Teléfono', max_chars=9, placeholder='Ingresa tu número de teléfono',
                                              label_visibility='hidden')
        if (user_signup_phone.isalpha() or len(user_signup_phone) < 9) and user_signup_phone:
            st.error(SIGNUP_PHONE_INVALID, icon="🚨")

        user_signup_password = st.text_input('Contraseña', type='password', placeholder="Ingresa tu contraseña")
        user_signup_password_verify = st.text_input('Repite tu contraseña', type='password', placeholder="Repite tu "
                                                                                                         "contraseña")

        if user_signup_password != user_signup_password_verify and user_signup_password_verify:
            st.error(SIGNUP_NOT_SAME_PASSWORD, icon="🚨")

        btn_signup = st.form_submit_button('Crear cuenta', use_container_width=True, type='primary')
        btn_goto_login = st.form_submit_button('Inicia sesión', use_container_width=True, type='secondary')

        if btn_signup:

            if not user_signup_name:
                st.error(SIGNUP_EMPTY_NAME, icon="🚨")
                st.stop()
            if not user_signup_lastname:
                st.error(SIGNUP_EMPTY_LASTNAME, icon="🚨")
                st.stop()
            if not user_signup_email:
                st.error(SIGNUP_EMPTY_EMAIL, icon="🚨")
                st.stop()
            if not user_signup_phone:
                st.error(SIGNUP_EMPTY_PHONE, icon="🚨")
                st.stop()
            if not user_signup_password:
                st.error(SIGNUP_EMPTY_PASSWORD, icon="🚨")
                st.stop()

            try:
                response = requests.post(f'{os.getenv("BASE_URL")}/inffia/api/v1/users/signup', json={
                    'email': user_signup_email,
                    'password': user_signup_password,
                    'phone': f"593{user_signup_phone}",
                    'first_name': user_signup_name,
                    'lastname': user_signup_lastname,
                })

                response_json = response.json()

                st.write(response_json)

                if response.status_code != 201:
                    st.error(response_json['detail'], icon="🚨")
                    st.stop()
                else:
                    st.session_state.current_user.userId = response_json['user_id']
                    st.session_state.current_user.accountId = response_json['account']['account_id']
                    st.session_state.current_form = 'verification_code'
                    st.rerun()

            except Exception as e:
                st.exception(e)

        if btn_goto_login:
            st.session_state.current_form = 'signin'
            st.rerun()


if __name__ == "__main__":
    sign_up_component()
