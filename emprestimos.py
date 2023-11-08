import streamlit as st
import requests
import pandas as pd
from api_permissions import get_token, check_status


def emprestimos():
    if check_status():
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        with open('style.css') as file:
            st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
          
            st.subheader('Empréstimos', divider='orange')
            
            # BARRA DE PESQUISA #
            searchBar_container = st.container()
            with searchBar_container:
                        
                url = 'https://rentup.up.railway.app/user/get-users'
                requestData = requests.get(url, headers=headers).json()
                df = pd.DataFrame.from_dict(requestData)

                array_nomes = df.values[:, 0]

                searchInput= st.selectbox('', array_nomes, index = None, placeholder="Buscar Usuário")
            
            
            # TABELA DE EMPRÉSTIMOS #
            st.warning("Tabela de empréstimos ainda não está disponível")
