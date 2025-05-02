from pages import Pages
from program import Program

import streamlit as st

def run():
    st.set_page_config('Predição de Produtos - BRF1', ':pill:')

    program = Program(st)
    app = Pages(st, program)
    pages = {
        'Mais Vendidos': app.main,
        'Predição': app.predict,
        'Dados': app.upload
    }

    with st.sidebar:
        menu = st.selectbox('Escolha a sua página', pages.keys())
        st.divider()

    pages[menu]()

if __name__ == "__main__":
    run()