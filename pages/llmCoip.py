import ast
import os
import time

import requests
import streamlit as st
import websocket

from errorConstants import LLM_COIP_NO_PASSAGES_FOUND
from menu import menu_with_redirect

global status_component

if "current_user" not in st.session_state or st.session_state.current_user.accessToken is None:
    st.switch_page('app.py')

# LOAD USER DATA
# LOAD USER CONVERSATION
response = requests.get(
    f'{os.getenv("BASE_URL")}/inffia/api/v1/conversations/all',
    headers={
        'Authorization': f'Bearer {st.session_state.current_user.accessToken}'
    }
)

response_json = response.json()
st.session_state.current_user.conversationId = response_json[0]['conversation_id']


def stream_data(ai_message):
    for word in ai_message.split(" "):
        yield word + " "
        time.sleep(0.02)


def on_message(ws, message):
    if message == 'End':
        ws.close()
        ws.keep_running = False
    elif str(message).startswith('final_inffia_response'):
        final_response = ast.literal_eval(message.split('final_inffia_response ')[-1])
        if len(final_response) == 0:
            st.session_state.messages.append({"role": "assistant", "content": LLM_COIP_NO_PASSAGES_FOUND})
            st.chat_message("assistant").write_stream(stream_data(LLM_COIP_NO_PASSAGES_FOUND))
        else:
            for prompt_response in final_response:
                ai_response = """
                    Según el artículo
                    
                    {current_law}
                    
                    {conflict}
                """.format(current_law=prompt_response['article'], conflict=prompt_response['conflict'])
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.chat_message("assistant").write_stream(stream_data(ai_response))
    else:
        status_component.write(message)
        status_component.update(label=message)


def on_error(ws, error):
    st.write(error)
    ws.close()
    ws.keep_running = False


def on_close(ws, close_status_code, close_msg):
    status_component.update(state='complete')


def on_open(ws):
    ws.send_text(str({
        'prompt': prompt,
        'similarity_percentage': similarity_percentage,
        'conversation_id': st.session_state.current_user.conversationId,
        'account_id': st.session_state.current_user.accountId
    }))
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write_stream(stream_data(prompt))
    global status_component
    status_component = st.status("Buscando leyes...")


menu_with_redirect()

with st.sidebar:
    st.divider()
    st.header('Porcentaje de similitud')
    similarity_percentage = st.slider(
        "El porcentaje de similitud es una forma de ajustar la sensibilidad del buscador de artículos del COIP que "
        "esten relacionados con la nueva propuesta de ley, permitiendote encontrar no solo el documento más similar, "
        "sino también aquellos que son solo parcialmente similares al texto buscado.",
        0, 100, 80)

    st.write('')

    if st.button("Cerrar Sesión", type="primary"):
        del st.session_state.current_user
        del st.session_state.messages
        st.switch_page('app.py')

st.title("🚀 COIP BOT")
st.caption("Realiza propuestas de ley y permite que chat bot encuentre conflicto con las leyes actuales")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, en que puedo ayudarte?"}]
    messages = requests.get(
        f'{os.getenv("BASE_URL")}/inffia/api/v1/conversations/messages/{st.session_state.current_user.conversationId}',
        headers={
            'Authorization': f'Bearer {st.session_state.current_user.accessToken}'
        }
    )
    messages_json = messages.json()

    for message in messages_json:
        st.session_state.messages.append({"role": "user", "content": message['user_message']})
        if message['ai_model_response'] == "":
            st.session_state.messages.append({"role": "assistant", "content": LLM_COIP_NO_PASSAGES_FOUND})
        else:
            st.session_state.messages.append({"role": "assistant", "content": message['ai_model_response']})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    header = {
        "Authorization": f"Bearer {st.session_state.current_user.accessToken}",
    }
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:8000/inffia/api/v1/messages/llm/coip/generate",
                                header=header,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
