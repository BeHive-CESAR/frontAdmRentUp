import streamlit as st
import requests
import pandas as pd
import json
from api_permissions import get_token, check_status


def usuarios():
    if check_status():
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        with open('style.css') as file:
            st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
          
        st.subheader('Usuários', divider='orange')
        
        if 'editarUsuario' not in st.session_state:
            st.session_state.editarUsuario = False

        # BARRA DE PESQUISA #
        searchBar_container = st.container()
        with searchBar_container:
    
            requestData = requests.get('https://rentup.up.railway.app/user/get-users', headers=headers).json()
        
            if requestData == 404:
                st.toast('Não há usuários cadastrados.')
            elif requestData == 401:
                st.toast('Não autorizado.')
            elif requestData == 403:
                st.toast('Token expirado. Faça login novamente.')
            else:
                df = pd.DataFrame.from_dict(requestData)

                array_emails = df.values[:, 0]
                
        
                searchInput= st.selectbox('', array_emails, index = None, placeholder="Buscar Usuário")
                if searchInput != None and st.session_state.editarUsuario == False:
                    st.session_state.editarUsuario = True
                
         
           
        # TABELA DOS USUÁRIOS #
        dataTable_container = st.container()
        with dataTable_container:
            if searchInput != None and st.session_state.editarUsuario == True:
                requestData = requests.get(f'https://rentup.up.railway.app/user/get-user-by-name?nome={searchInput}', headers=headers).json()

                email = requestData[0]['email']	
                cargo = requestData[0]['role']

                with st.form("Editar Usuario", True):
                    st.text('Editar Usuário')
                
                    role = st.selectbox('Cargo', ['ADMINISTRATOR', 'USER'], placeholder=cargo, index= None)

                    cols = st.columns([5.5,1,0.8])  

                    with cols[1]:
                        cancel = st.form_submit_button("Cancelar")
                        if cancel:
                            st.session_state.editarUsuario = False
                           
                    with cols[2]:
                        submit_button = st.form_submit_button('Salvar')

                    if submit_button:
                        requestData = requests.put(f'https://rentup.up.railway.app/user/edit-role?email={email}&role={role}', headers=headers)
                        st.toast('Usuário editado com sucesso!')
                        st.session_state.editarUsuario = False
                        #st.rerun()

                cols = st.columns([4.5,1])

                with cols[1]:
                    if st.button('Excluir Usuário'):
                        requestData = requests.delete(f'https://rentup.up.railway.app/user/delete-user?email={email}', headers=headers)
                        st.toast('Usuário excluído com sucesso!')
                        st.session_state.editarUsuario = False
                        st.rerun()
            else:
                requestData = requests.get('https://rentup.up.railway.app/user/get-users', headers=headers).json()
                
                df = pd.DataFrame.from_dict(requestData)
                df.columns = ['Nome', 'Email', 'Contato', 'Cargo']
                st.dataframe(df,hide_index=True,width=1000) 
    else:
        st.alert('Você não está logado, faça login para acessar essa página.') 