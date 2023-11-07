import streamlit as st
import inventario, dashboard
import json, os
from PIL import Image
import requests
from api_permissions import check_status

# admin@admin.com
# admin 


# FUNÇÃO DE LOGIN
def login():
    st.warning('Adminstrador ou usuário: email = "admin@admin.com",  senha = "admin"')
    tipo = st.selectbox('Tipo de usuário', ('Administrador', 'Aluno ou Professor'))

    #Se for aluno ou professor, redireciona para a outra aplicação
    if tipo == 'Aluno ou Professor':
        st.link_button("Fazer login como Aluno ou Professor", "https://rentup-user.streamlit.app")

    #Se for administrador, pede pra preencher o forms de login
    else:
        with st.form("loginForms", True):
            email = st.text_input('Email')    
            senha = st.text_input('Senha',  type="password")
          
            submitted = st.form_submit_button("Enviar")
            if submitted: 
                url = 'https://mockapi.up.railway.app/user/login'

                data = {
                    "email": email,
                    "password": senha
                }
                
                response = requests.post(url, json=data)

                if response.status_code == 200:
                    output = response.json()
                    with open("auth_user", "w") as json_file:
                        json.dump(output, json_file)
                    with open("auth_user_data", "w") as json_file:
                        json.dump(data, json_file)

                    st.rerun()
                else:
                    st.error("Credenciais Inválidas")
                
# Se o usuário já estiver logado, o forms de login não aparecerá
if check_status():
    #Definindo a sidebar global da interface do adm
    with st.sidebar:
        page = st.selectbox('Selecione uma página:', ('Inventário', 'Dashboard'))

        #Se o usuário deslogar, o arquivo json é removido e pede para fazer login novamente
        if st.button("Logout"):
            os.remove('auth_user')
            os.remove('auth_user_data')
            st.rerun()

    if page == 'Dashboard':
        dashboard.dashboard()
    elif page == 'Inventário':
        inventario.inventario()

# Enquanto o usuário não estiver logado, irá pedir para preencher o forms de  login
else:
    # HEADER DO SITE #
    logo_container = st.container()
    col1, col2, col3 = st.columns(3)

    with logo_container:
        with col2:
            image = Image.open('img/logo.png')
            st.image(image, width=150)
            
    login()