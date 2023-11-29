import streamlit as st
import requests
import pandas as pd
from api_permissions import get_token


def inventario():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
    
        if 'adicionarItem' not in st.session_state:
            st.session_state.adicionarItem = False
        if 'editarItem' not in st.session_state:
            st.session_state.editarItem = False

        st.subheader('Inventário', divider='orange')

        
        # BARRA DE PESQUISA #
        searchBar_container = st.container()
        with searchBar_container:
            col1, col2 = st.columns([5, 1])
        
            with col1:
                url = 'https://rentup.up.railway.app/item/get-items'
                requestData = requests.get(url, headers=headers).json()
                error_message = requestData.get('detail')
                
                if requestData != 200:
                    st.error(error_message)
        
                    
                df = pd.DataFrame.from_dict(requestData["itens"])

                array_nomes = df.values[:, 0]

                searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Item")

                if searchInput != None and st.session_state.editarItem == False:
                    st.session_state.editarItem = True
                

            with col2:
                if st.session_state.editarItem == True and searchInput != None:
           
                    if st.button("Deletar", use_container_width=True, type= "primary"):
                        
                        url = 'https://rentup.up.railway.app/item/delete-item'
                        
                        data = {
                            "nome": searchInput
                        }

                        response = requests.delete(url, json=data,headers=headers)
                        error_message = response.json().get('detail')
                        
                        if response.status_code == 204:
                            st.toast('Item excluído com sucesso', icon="✅")
                            st.rerun()
                        else:   
                            st.toast(error_message, icon="⚠️")
                else:
                    if st.button("Adicionar", use_container_width=True, type= "secondary"):
                        st.session_state.adicionarItem = True

        #Form de adicionar um item
        if st.session_state.adicionarItem == True:
            with st.form("Adicionar", True):
                
                st.text("Adicionar item")
                
                nome = st.text_input('Nome')
                estoque = st.number_input('Estoque', step=1)
                emprestimo = st.number_input('Emprestáveis', step=1)
                emprestados = st.number_input('Emprestados',  step=1)
                quebrados = st.number_input('Quebrados', step=1)
                descricao = st.text_input('Descrição')
                imagem = st.text_input('URL da imagem')

        
                cols = st.columns([5.5,1,0.8])
                
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
                        "qntEstoque": estoque,
                        "qntEmprestar": emprestimo,
                        "qntEmprestados": emprestados,
                        "qntDanificados": quebrados,
                        "descricao": descricao,
                        "imagem": imagem
                    }

                    url = 'https://rentup.up.railway.app/item/create-item'
                    response = requests.post(url, json=data, headers=headers)
                    error_message = response.json().get('detail')
                    
                    if response.status_code == 201:
                        st.toast('Item adicionado com sucesso', icon="✅")
                        st.session_state.adicionarItem = False
                        st.rerun()
                    else:
                        st.toast(error_message, icon="⚠️")
                             
        # FORMS DE EDITAR UM ITEM #
        if st.session_state.editarItem == True and searchInput != None:  
            url = f'https://rentup.up.railway.app/item/get-item-by-name?item={searchInput}'
            response = requests.get(url,headers=headers)
                
            if response.status_code == 404 and st.session_state.editarItem == True and searchInput != None:
                st.error("Nenhum item com o nome especificado foi encontrado no estoque.")
            elif response.status_code == 403:
                st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
            else:
                with st.form("Editar", True):
                    st.text("Editar Item")
                    item = response.json()['item']
                    
                    nome = st.text_input('Nome', value = item["nome_item"])
                    estoque = st.number_input('Estoque', value =  item["qnt_estoque"], step=1)
                    emprestimo = st.number_input('Emprestáveis', value =  item["qnt_emprestar"], step=1)
                    emprestados = st.number_input('Emprestados', value =  item["qnt_emprestados"], step=1)
                    quebrados = st.number_input('Quebrados',value =  item["qnt_danificados"],  step=1)
                    descricao = st.text_input('Descrição', value=  item["descricao"])      
                    imagem = st.text_input('URL da Imagem')

                    cols = st.columns([5.5,1,0.8])  
        
                    with cols[1]:
                        cancel = st.form_submit_button("Cancelar")

                    with cols[2]:
                        submitted = st.form_submit_button("Salvar")

                    if cancel:
                        st.session_state.editarItem = False

                    
                    if submitted:
                        data = {                  
                            "item1": {
                                "nome": item["nome_item"]
                            },
                            "item2": {
                                "nome": nome,
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
                        error_message = response.json().get('detail')
                        
                        if response == 200:
                            st.toast('Item adicionado com sucesso', icon="✅")
                        else:
                            st.error(error_message)
                                                 
        # TABELA DOS ITENS #        
        dataTable_container = st.container()
        with dataTable_container:
            
            url = 'https://rentup.up.railway.app/item/get-items'
            requestData = requests.get(url, headers=headers).json()
            error_message = requestData.json().get('detail')

        
        if requestData == 404:
            st.error(error_message)

        elif requestData == 403:
            st.error(error_message)

        else:
            df = pd.DataFrame.from_dict(requestData["itens"])
            df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição', 'Imagem']
            df = df.drop(columns=['Imagem'])
            
            if searchInput != None and st.session_state.editarItem == True:
                response = requests.get(f"https://rentup.up.railway.app/item/get-item-by-name?item={searchInput}", headers=headers)
                error_message = response.json().get('detail')
              
                if response == 200:
                    item = response.json()['item']

                    df = pd.DataFrame([item])
                    df.columns = ['Item', 'Total', 'Em estoque', 'Emprestáveis', 'Emprestados', 'Quebrados', 'Descrição', 'Imagem']
                    df = df.drop(columns=['Imagem'])
                else:
                    error_message = response.json().get('detail')
            
             # Criar DataFrame
            st.dataframe(df,hide_index=True,width=1000) 
            
    

                            
                            