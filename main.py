import streamlit as st
import inventario, dashboard
import json, os
from PIL import Image
import requests
from api_permissions import check_status

# Adminstrador: [admin@admin.com] e [admin]
# Usuário: [user@user.com] e [user]

# FUNÇÃO DE LOGIN
def login():

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

                if response.status_code == 200: #Se o usuário for logado com sucesso 
                    output = response.json()
                    with open("auth_user", "w") as json_file: #Escrevendo os dados do usuário em um json
                        json.dump(output, json_file)

                    with open("auth_user_data", "w") as json_file: #Escrevendo os dados (apenas o email e a senha inserida) do usuário em um json
                        json.dump(data, json_file)

                    #Verificando se o tipo inserido condiz com o banco de dados
                    with open("auth_user", "r") as json_file: 
                        output = json.load(json_file)  

                    user_tipe = output['access']

                    if user_tipe != "ADMINISTRATOR":
                        os.remove('auth_user')
                        os.remove('auth_user_data')
                        st.error("Tipo de usuário informado não condiz com o nosso sistema")
                    else:
                        st.rerun()
                else:
                    st.error("Credenciais Inválidas")
                    
        if st.button("Cadastro"):
            st.session_state.cadastro = True
            st.rerun()

def cadastro():
    #Se for administrador, pede pra preencher o forms de login
    with st.form("RegisterForms", True):
        email = st.text_input('Email')    
        password = st.text_input('Senha',  type="password")
        name = st.text_input('Nome')  
        number = st.text_input('Número')  

        submitted = st.form_submit_button("Enviar")
        
        if submitted: 
            url = 'https://mockapi.up.railway.app/user/register'

            data = {
                "email": email,
                "password": password,
                "name": name,
                "role": "USER",
                "number": number
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200: #Se o usuário for logado com sucesso 
                st.session_state.cadastro = False
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
                
    if st.button("Login"):
        st.session_state.cadastro = False
        st.rerun()
    
if 'cadastro' not in st.session_state:
    st.session_state.cadastro = False

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
    
    if st.session_state.cadastro == False:
        login()
        
    else:
        cadastro()


    
    
    