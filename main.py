import streamlit as st
import inventario, dashboard, usuarios
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
              
                data = {
                    "email": email,
                    "password": senha
                }

                response = requests.post("https://rentup.up.railway.app/user/login", json=data)
                
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
        contato = st.text_input('Número') 
        nome = st.text_input('Nome')  
        password = st.text_input('Senha',  type="password")
        st.caption('A senha deve conter uma letra maiúscula e um caractere especial')
        
        cols = st.columns([4,1,1])

        with cols[1]:
            submitted = st.form_submit_button("Cadastrar")
            
            if submitted: 
                url = 'https://rentup.up.railway.app/user/register'

                data = {
                    "email": email,
                    "password": password,
                    "nome": nome,
                    "contato": contato,
                    "cargo": "USER",
                    
                }
                
                response = requests.post(url, json=data)
                
                if response.status_code == 201: #Se o usuário for logado com sucesso 
                    st.session_state.cadastro = False
                    st.rerun()
                elif response.status_code == 400:
                    st.error('A solicitação de registro não atende aos requisitos')
                elif response.status_code == 409:
                    st.error('Conflito de dados. O endereço de e-mail já está em uso por outro usuário.')
                else:
                    st.error("Credenciais Inválidas")
                    
        with cols[2]:    
            if st.form_submit_button("Cancelar"):
                st.session_state.cadastro = False
                st.rerun()
    
if 'cadastro' not in st.session_state:
    st.session_state.cadastro = False

# Se o usuário já estiver logado, o forms de login não aparecerá
if check_status():
    #Definindo a sidebar global da interface do adm
    with st.sidebar:
        logo_container = st.container()
        
        with logo_container: 
            image = Image.open('img/logo.png')
            st.image(image, width=150)
            
        st.markdown("##")
        
        page = st.selectbox('Selecione uma página:', ('Usuário', 'Dashboard'))

        #Se o usuário deslogar, o arquivo json é removido e pede para fazer login novamente
        if st.button("Logout"):
            os.remove('auth_user')
            os.remove('auth_user_data')
            st.rerun()

    if page == 'Dashboard':
        dashboard.dashboard()
    # elif page == 'Inventário':
    #     inventario.inventario()
    elif page == 'Usuário':
        usuarios.usuarios()
        

# Enquanto o usuário não estiver logado, irá pedir para preencher o forms de  login
else:
    # HEADER DO SITE #
    if st.session_state.cadastro == False:
        login()  
    else:
        cadastro()


    
    
    