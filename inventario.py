import streamlit as st
import requests
import pandas as pd
from api_permissions import get_token, check_status


def inventario():
    if check_status():
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        with open('style.css') as file:
            st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
        
            if 'adicionarItem' not in st.session_state:
                st.session_state.adicionarItem = False

            st.subheader('Inventário', divider='orange')

            
            # BARRA DE PESQUISA #
            searchBar_container = st.container()
            with searchBar_container:
                col1, col2 = st.columns([5, 1])
            
                with col1:
                    url = 'https://rentup.up.railway.app/item/get-items'
                    requestData = requests.get(url, headers=headers).json()

                    if requestData != 200:
                        if requestData == 404:
                            st.error("Não foram encontrados itens no estoque")
                        elif requestData == 403:
                            st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
                    
                    df = pd.DataFrame.from_dict(requestData["itens"])

                    array_nomes = df.values[:, 0]

                    searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Item")
                with col2:
                    if st.button("Adicionar", use_container_width=True):
                        st.session_state.adicionarItem = True
                        #st.rerun()

            if st.session_state.adicionarItem == True:
                with st.form("Adicionar", True):
                    
                    st.text("Adicionar item")
                    
                    nome = st.text_input('Nome')
                    total = st.number_input('Total', step=1)
                    estoque = st.number_input('Estoque', step=1)
                    emprestimo = st.number_input('Emprestáveis', step=1)
                    emprestados = st.number_input('Emprestados',  step=1)
                    quebrados = st.number_input('Quebrados', step=1)
                    descricao = st.text_input('Descrição')
                    imagem = st.text_input('URL da imagem')

            
                    cols = st.columns([5,1,1])
                    
                    with cols[1]:
                        cancel = st.form_submit_button("Cancelar")
                        if cancel:
                            st.session_state.adicionarItem = False
                            st.rerun()
                        
                    with cols[2]:
                        submitted = st.form_submit_button("Enviar")
                        
                    if submitted:
                        data = {     
                            "nome": nome,
                            "qntTotal": total,
                            "qntEstoque": estoque,
                            "qntEmprestar": emprestimo,
                            "qntEmprestados": emprestados,
                            "qntDanificados": quebrados,
                            "descricao": descricao,
                            "imagem": imagem
                        }

                        url = 'https://rentup.up.railway.app/item/create-item'
                        response = requests.post(url, json=data, headers=headers)

                        if response == 201:
                            st.session_state.adicionarItem = False
                            st.rerun()
                        elif response == 400:
                            st.error("A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).")
                        elif response == 401:
                            st.error("Acesso não autorizado. Somente administradores podem criar itens.")
                        elif response == 403:
                            st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
                            
                
                    
        
            
            # FORMS DE EDITAR UM ITEM #
            if searchInput != None:  
                
                with st.form("Editar", clear_on_submit=False):
                    st.text("Editar Item")

                    url = f'https://rentup.up.railway.app/item/get-item-by-name?item={searchInput}'
                    response = requests.get(url,headers=headers)
                    
                    if response != 200:
                        if response == 404:
                            st.error("Nenhum item com o nome especificado foi encontrado no estoque.")
                        elif response == 403:
                            st.error("Falha na autenticação. O token de acesso fornecido não é válido.")

                    item = response.json()['item']
                    

                    
                    nome = st.text_input('Nome', value = item["nome_item"])
                    total = st.number_input('Total', value = item["qnt_total"], step=1)
                    estoque = st.number_input('Estoque', value =  item["qnt_estoque"], step=1)
                    emprestimo = st.number_input('Emprestáveis', value =  item["qnt_emprestar"], step=1)
                    emprestados = st.number_input('Emprestados', value =  item["qnt_emprestados"], step=1)
                    quebrados = st.number_input('Quebrados',value =  item["qnt_danificados"],  step=1)
                    descricao = st.text_input('Descrição', value=  item["descricao"])      
                    imagem = st.text_input('URL da Imagem')

                    cols = st.columns([5,1.5,1,1])    
                    with cols[2]:
                        if st.form_submit_button("Deletar"):  
                            url = 'https://rentup.up.railway.app/item/delete-item'
                            
                            data = {
                                "nome": searchInput
                            }

                            response = requests.delete(url, json=data,headers=headers)

                            if response.status_code == 200:
                                st.rerun()
                            elif response.status_code == 400:
                                st.error("A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).")
                            elif response.status_code == 401:
                                st.error(" Acesso não autorizado. Somente administradores podem criar itens.")
                            elif response.status_code == 403:
                                st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
                            elif response.status_code == 404:
                                st.error(" Nenhum item com o nome especificado foi encontrado no estoque.")

                    with cols[3]:
                        if st.form_submit_button("Salvar"):
                            data = {                  
                                "item1": {
                                    "nome": item["nome_item"]
                                },
                                "item2": {
                                    "nome": nome,
                                    "qntTotal": total,
                                    "qntEstoque": estoque,
                                    "qntEmprestar": emprestimo,
                                    "qntEmprestados": emprestados,
                                    "qntDanificados": quebrados,
                                    "descricao": descricao,
                                    "imagem": imagem
                                }
                            }

                            url = 'https://rentup.up.railway.app/item/edit-item'
                            response = requests.put(url, json=data,headers=headers)
                            
                            if response == 200:
                                st.toast('Item adicionado com sucesso', icon="✅")
                            elif response == 400:
                                st.error("A solicitação não atende aos requisitos (por exemplo, campos em branco, formato inválido).")
                            elif response == 401:
                                st.error("Acesso não autorizado. Somente administradores podem criar itens.")
                            elif response == 403:
                                st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
                            elif response == 404:
                                st.error("Nenhum item com o nome original especificado foi encontrado no estoque.")


            # TABELA DOS ITENS #        
            dataTable_container = st.container()
            with dataTable_container:
                
                url = 'https://rentup.up.railway.app/item/get-items'
                requestData = requests.get(url, headers=headers).json()
                
                if requestData != 200:
                    if requestData == 404:
                        st.error("Não foram encontrados itens no estoque.")
                    elif requestData == 403:
                        st.error("Falha na autenticação. O token de acesso fornecido não é válido.")

                df = pd.DataFrame.from_dict(requestData["itens"])
                df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição', 'Imagem']

                if searchInput != None:
                    response = requests.get(f"https://rentup.up.railway.app/item/get-item-by-name?item={searchInput}", headers=headers)

                    if response != 200:
                        if response == 404:
                            st.error("Nenhum item com o nome especificado foi encontrado no estoque.")
                        elif response == 403:
                            st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
                    
                    item = response.json()['item']

                    df = pd.DataFrame([item])
                    df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição', 'Imagem']
                
                
                # Criar DataFrame
                st.dataframe(df,hide_index=True,width=1000) 
    else:
        st.alert('Você não está logado, faça login para acessar essa página.')

                            
                            
