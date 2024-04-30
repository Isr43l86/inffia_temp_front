import os

import requests
import streamlit as st

from appConstants import MESSAGES_EMAIL_VERIFIED_SUCCESS


def verify_email_component():
    with st.form('Login', clear_on_submit=True):
        st.header('Verifica tu cuenta')
        st.markdown('Ingresa el código de verificación que ha sido enviado a tu correo')
        user_verification_code = st.text_input("Código de verificación",
                                               placeholder="Ingresa el código de verificación que recibiste")
        btn_verify_account = st.form_submit_button('Verificar cuenta', use_container_width=True, type='primary')
        if btn_verify_account:
            try:
                response = requests.post(
                    f'{os.getenv("BASE_URL")}/inffia/api/v1/accounts/verification/'
                    f'{st.session_state.current_user.accountId}/{user_verification_code}'
                )
                response = response.json()
                st.session_state.current_user.accessToken = response['access_token']
                st.success(MESSAGES_EMAIL_VERIFIED_SUCCESS, icon="✅")
            except Exception as e:
                st.exception(e)


if __name__ == "__main__":
    verify_email_component()
