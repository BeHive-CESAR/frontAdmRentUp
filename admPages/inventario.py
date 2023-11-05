import streamlit as st
import requests
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px


def inventario():

    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)


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
        url = 'https://mockapi.up.railway.app/get_itens'
        requestData = requests.get(url).json()
        df = pd.DataFrame.from_dict(requestData)
        array_nomes = df.values[:, 0]

        searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Item")
        
        editInput= st.selectbox('', array_nomes, index = None, placeholder="Editar Item", key = 'selection')
        if editInput != None:
            with st.form("Editar", clear_on_submit=False):
                url = f'https://mockapi.up.railway.app/get_item?nome_item={editInput}'
                response = requests.get(url)
                item = response.json()

                nome = st.text_input('Nome', value= item["item"])
                total = st.number_input('Total', value = item["qnt_total"], step=1)
                estoque = st.number_input('Estoque', value = item["qnt_estoque"], step=1)
                emprestimo = st.number_input('Emprestáveis', value = item["qnt_emprestimo"], step=1)
                emprestados = st.number_input('Emprestados', value = item["qnt_emprestados"], step=1)
                quebrados = st.number_input('Quebrados',value = item["qnt_quebrados"],  step=1)
                descricao = st.text_input('Descrição', value= item["descricao"])
            
                submitted = st.form_submit_button("Enviar")
                if submitted:
                    data = {
                        "item": {
                            "item": item["item"],
                            "qnt_total": item["qnt_total"],
                            "qnt_estoque": item["qnt_estoque"],
                            "qnt_emprestimo": item["qnt_emprestimo"],
                            "qnt_emprestados": item["qnt_emprestados"],
                            "qnt_quebrados": item["qnt_quebrados"],
                            "descricao": item["descricao"]
                        },
                        "item2": {
                            "item": item["item"],
                            "qnt_total": total,
                            "qnt_estoque": estoque,
                            "qnt_emprestimo": emprestimo,
                            "qnt_emprestados": emprestados,
                            "qnt_quebrados": quebrados,
                            "descricao": descricao
                        }
                    }

                    url = 'https://mockapi.up.railway.app/edit_item'
                    response = requests.put(url, json=data)
                        


        # FORMS DE ADICIONAR UM ITEM #
        with st.expander("Adicionar Item"):
            with st.form("Adicionar", True):
                url = 'https://mockapi.up.railway.app/post_item'
                nome = st.text_input('Nome')
                total = st.number_input('Total', step=1)
                estoque = st.number_input('Estoque', step=1)
                emprestimo = st.number_input('Emprestáveis', step=1)
                emprestados = st.number_input('Emprestados',  step=1)
                quebrados = st.number_input('Quebrados', step=1)
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


        if searchInput != None:
            df = df[df["Item"].isin([searchInput])]
        
        st.dataframe(df,hide_index=True,width=1000) 