import streamlit as st


def authenticated_menu():
    st.sidebar.title("LLM's")
    st.sidebar.page_link("pages/llmCoip.py", label="COIP LLM")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Login")


def menu():
    if "current_user" not in st.session_state or st.session_state.current_user.accessToken is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "current_user" not in st.session_state or st.session_state.current_user.accessToken is None:
        st.switch_page("app.py")
    menu()
