import os
import time

import requests
import streamlit as st

from appConstants import MESSAGES_EMAIL_VERIFIED_SUCCESS
from errorConstants import SIGNUP_EMPTY_VERIFY_CODE


def verify_email_component():
    with st.form('Login', clear_on_submit=True):
        st.header('Verifica tu cuenta')
        st.markdown('Ingresa el código de verificación que ha sido enviado a tu correo')
        user_verification_code = st.text_input("Código de verificación",
                                               placeholder="Ingresa el código de verificación que recibiste")
        btn_verify_account = st.form_submit_button('Verificar cuenta', use_container_width=True, type='primary')
        if btn_verify_account:

            if not user_verification_code:
                st.error(SIGNUP_EMPTY_VERIFY_CODE, icon="🚨")
                st.stop()

            try:
                response = requests.post(
                    f'{os.getenv("BASE_URL")}/inffia/api/v1/accounts/verification/'
                    f'{st.session_state.current_user.accountId}/{user_verification_code}'
                )
                response_json = response.json()

                if response.status_code != 200:
                    st.error(response_json['detail'].split(':')[-1].strip(), icon="🚨")
                else:
                    st.session_state.current_user.accessToken = response_json['access_token']
                    st.success(MESSAGES_EMAIL_VERIFIED_SUCCESS, icon="✅")
                    time.sleep(3)
                    st.switch_page("pages/llmCoip.py")
            except Exception as e:
                st.exception(e)


if __name__ == "__main__":
    verify_email_component()
