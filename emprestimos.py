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

            if requestData != 200:
                if requestData == 404:
                    st.error("Não foram encontrados usuários no sistema.")
                elif requestData == 401:
                    st.error("Acesso negado. O usuário não tem permissão para acessar este recurso.")
                elif requestData == 403:
                    st.error("Falha na autenticação. O token de acesso fornecido não é válido.")
            
            df = pd.DataFrame.from_dict(requestData)

            array_emails = []

            for index, row in df.iterrows():
                array_emails.append(row['email'])

            searchInput= st.selectbox('', array_emails, index = None, placeholder="Buscar Usuário")
        
        
        # TABELA DE EMPRÉSTIMOS #
        if searchInput != None:
            response = requests.get(f"https://rentup.up.railway.app/rent/history-user?user_email={searchInput}", headers=headers)


            if response.status_code == 200:
                response = response.json()
                df = pd.DataFrame.from_dict(response["rents"])
                df.columns = ['ID', 'Usuário', 'Item', 'Data do Empréstimo', 'Data da Devolução', 'Status']
                st.dataframe(df,hide_index=True,width=1000) 

            elif response.status_code == 403:
                st.error("Acesso não autorizado. O usuário não está autenticado.")
            elif response.status_code == 404:
                st.error("Nenhum empréstimo encontrado para o usuário especificado.")
        

        else:
            response = requests.get("https://rentup.up.railway.app/rent/history", headers=headers)

            if response.status_code == 200:
                historico_emprestimos = response.json()
                df = pd.DataFrame.from_dict(historico_emprestimos)

                df.columns = ['ID', 'Usuário', 'Item', 'Data do Empréstimo', 'Data da Devolução', 'Status']
                st.dataframe(df,hide_index=True,width=1000) 
            else:
                print("Nenhum registro de empréstimo encontrado no sistema. Verifique suas permissões de administrador.")
    else:
        st.alert('Você não está logado, faça login para acessar essa página.')      
            