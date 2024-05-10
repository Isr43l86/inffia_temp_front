import streamlit as st


def load_conversations_page():
    code = """
        <ul>
        {% for thing in {options} %}
          <li>{{ thing.name }}</li>
        {% endfor %}  
        </ul>
    """

    st.code(code.format(options=["opcion 1", "opcion 2"]))


if __name__ == "__main__":
    load_conversations_page()
