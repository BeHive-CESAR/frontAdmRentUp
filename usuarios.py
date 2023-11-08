import streamlit as st
import requests
from PIL import Image
import pandas as pd
import json
import os
from api_permissions import get_token, check_status


def usuarios():
    if check_status():
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        with open('style.css') as file:
            st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
          
            st.subheader('Usuário', divider='orange')
            
            # BARRA DE PESQUISA #
            searchBar_container = st.container()
            with searchBar_container:
                        
                url = 'https://rentup.up.railway.app/user/get-users'
                requestData = requests.get(url, headers=headers).json()
                df = pd.DataFrame.from_dict(requestData)

                array_nomes = df.values[:, 0]

                searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Usuário")
            
            
            # TABELA DOS USUÁRIOS #
            dataTable_container = st.container()
            with dataTable_container:

                if searchInput != None:
                    requestData = requests.get(f'https://rentup.up.railway.app/user/get-user-by-name?nome={searchInput}', headers=headers).json()
                
                else:
                    requestData = requests.get(url, headers=headers).json()  
                
                df = pd.DataFrame.from_dict(requestData)
                df.columns = ['Nome', 'Email', 'Contato', 'Cargo']
                st.dataframe(df,hide_index=True,width=1000) 
        