import streamlit as st
import requests
import pandas as pd
from api_permissions import get_token


def inventario():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
        
        st.subheader('Inventário', divider='orange')
        
        adicionarItem = False
        
        # BARRA DE PESQUISA #
        searchBar_container = st.container()
        with searchBar_container:
            col1, col2 = st.columns([5, 1])
        
            with col1:
                url = 'https://mockapi.up.railway.app/item/get_itens'
                requestData = requests.get(url, headers=headers).json()
                df = pd.DataFrame.from_dict(requestData)

                array_nomes = df.values[:, 0]

                searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Item")
            with col2:
                if st.button("Adicionar", use_container_width=True):
                    adicionarItem = True

        if adicionarItem:
            with st.form("Adicionar", True):
                url = 'https://mockapi.up.railway.app/item/post_item'
                
                st.text("Adicionar item")
                
                nome = st.text_input('Nome')
                total = st.number_input('Total', step=1)
                estoque = st.number_input('Estoque', step=1)
                emprestimo = st.number_input('Emprestáveis', step=1)
                emprestados = st.number_input('Emprestados',  step=1)
                quebrados = st.number_input('Quebrados', step=1)
                descricao = st.text_input('Descrição')

            # Every form must have a submit button.
                cols = st.columns([5,1,1])
                
                with cols[1]:
                    cancel = st.form_submit_button("Cancelar")
                    
                with cols[2]:
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
                    response = requests.post(url, json=data, headers=headers)

                    if response == 200:
                        st.toast('Item adicionado com sucesso', icon="✅")
                
                elif cancel:
                    st.rerun()
        
        
        # TABELA DOS ITENS #
        url = 'https://mockapi.up.railway.app/item/get_itens'
        dataTable_container = st.container()
        with dataTable_container:
        
            requestData = requests.get(url, headers=headers).json()
            

            df = pd.DataFrame.from_dict(requestData)
            df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição']


            if searchInput != None:
                df = df[df["Item"].isin([searchInput])]
            
            st.dataframe(df,hide_index=True,width=1000) 
            
            if searchInput != None:              
                # FORMS DE EDITAR UM ITEM #
                with st.form("Editar", clear_on_submit=False):
                    url = f'https://mockapi.up.railway.app/item/get_item?nome_item={searchInput}'
                    response = requests.get(url,headers=headers)
                    item = response.json()

                    st.write("Editar Item")
                    
                    nome = st.text_input('Nome', value= item["item"])
                    total = st.number_input('Total', value = item["qnt_total"], step=1)
                    estoque = st.number_input('Estoque', value = item["qnt_estoque"], step=1)
                    emprestimo = st.number_input('Emprestáveis', value = item["qnt_emprestimo"], step=1)
                    emprestados = st.number_input('Emprestados', value = item["qnt_emprestados"], step=1)
                    quebrados = st.number_input('Quebrados',value = item["qnt_quebrados"],  step=1)
                    descricao = st.text_input('Descrição', value= item["descricao"])
                
                    submitted = st.form_submit_button("Salvar")
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

                        url = 'https://mockapi.up.railway.app/item/edit_item'
                        response = requests.put(url, json=data,headers=headers)
                        if response == 200:
                            st.toast('Item editado com sucesso', icon="✅")
