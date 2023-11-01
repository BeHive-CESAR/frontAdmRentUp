import streamlit as st
import requests
from PIL import Image
import pandas as pd
import numpy as np

#streamlit run myfile.py

with open('style.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# SIDE BAR #
with st.sidebar:
    st.markdown("##")
    st.text("Olá, Fulano!")


# HEADER DO SITE #
logo_container = st.container()
col1, col2, col3 = st.columns(3)

with logo_container:
    with col2:
        image = Image.open('img/logo.png')
        st.image(image, width=150)
 
st.subheader('Inventário', divider='orange')

searchBar_container = st.container()
with searchBar_container:

    # BARRA DE PESQUISA #
    searchInput = st.text_input("",placeholder="Buscar Item")
    
    # FORMS DE ADICIONAR ITEM #
    with st.expander("Adicionar Item"):
        with st.form("Adicionar", True):
            url = 'https://mockapi.up.railway.app/post-item'
            nome = st.text_input('Nome')
            total = st.number_input('Total', value = None, step=1)
            estoque = st.number_input('Estoque', value = None, step=1)
            emprestimo = st.number_input('Emprestáveis', value = None,step=1)
            emprestados = st.number_input('Emprestados', value = None, step=1)
            quebrados = st.number_input('Quebrados',value = None, step=1)
            descricao = st.text_input('Descrição')

        # Every form must have a submit button.
            submitted = st.form_submit_button("Enviar")
            if submitted:
                    data = {
                        "item" : nome,
                        "qnt_total": total,
                        "qnt_estoque": estoque,
                        "qnt_emprestimo": emprestimo,
                        "qnt_emprestados": emprestados,
                        "qnt_quebrados": quebrados,
                        "descricao": descricao
                    }
                    response = requests.post(url, json=data)


st.markdown("##")

url = 'https://mockapi.up.railway.app/get_itens'

# TABELA DOS ITENS #
dataTable_container = st.container()
with dataTable_container:
   
    requestData = requests.get(url).json()

    df = pd.DataFrame.from_dict(requestData)
    df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição']

    stripInput = searchInput.strip()
    if stripInput != "":
        df = df[df["Item"].isin([searchInput])]
    
    st.dataframe(df,hide_index=True,) 

        
