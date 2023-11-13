import streamlit as st
import dashboard, inventario, usuarios, emprestimos
import json, os
from PIL import Image
import requests
from api_permissions import check_status

# Adminstrador: [admin@cesar.school] e [Admin123@]
# Usuário: [user@user.com] e [User100%]

def login(): # FUNÇÃO DE LOGIN
    
    with open('style.css') as file: #Importando arquivo css
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

    logo_container = st.container() # LOGO #
    with logo_container: 
        logo_cols = st.columns([1,1,1])
        with logo_cols[1]:
            image = Image.open('img/logo.png')
            st.image(image, width=150)
    
    st.header('Login', divider='orange')
    
    tipo = st.selectbox('Tipo de usuário', ('Administrador', 'Aluno ou Professor'))
    if tipo == 'Aluno ou Professor':
        st.link_button("Fazer login como Aluno ou Professor", "https://rentup-user.streamlit.app")
    
    else:
        with st.form("loginForms", True):  #Forms de login#
            email = st.text_input('Email')    
            senha = st.text_input('Senha',  type="password")

            login_cols = st.columns([5,2.5,1])    
            with login_cols[2]:
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

                    
                    with open("auth_user", "r") as json_file: #Verificando se o tipo inserido condiz com o banco de dados 
                        output = json.load(json_file)  

                    user_tipe = output['access']

                    if user_tipe != "ADMINISTRATOR":
                        os.remove('auth_user')
                        st.error("Tipo de usuário informado não condiz com o nosso sistema")
                    else:
                        st.rerun()
                else:
                    st.error("Credenciais Inválidas")

        cancel_cols = st.columns([6, 1])                
        with cancel_cols[1]:
            if st.button("Cadastro", type='secondary'):
                st.session_state.cadastro = True
                st.rerun()


def cadastro(): #Função de cadastro
    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
        
    
    logo_container = st.container() # LOGO #
    with logo_container: 
        logo_cols = st.columns([1,1,1])
        with logo_cols[1]:
            image = Image.open('img/logo.png')
            st.image(image, width=150)

    st.header('Cadastro', divider='orange')
    
    with st.form("RegisterForms", True): #Se for administrador, pede pra preencher o forms de login
        email = st.text_input('Email')    
        contato = st.text_input('Número') 
        nome = st.text_input('Nome')  
        password = st.text_input('Senha',  type="password")
        st.caption('A senha deve conter uma letra maiúscula e um caractere especial')
        
        cols = st.columns([5,1,0.8])        
        
        with cols[1]:    
            if st.form_submit_button("Cancelar"):
                st.session_state.cadastro = False
                st.rerun()
    
        with cols[2]:
            submitted = st.form_submit_button("Enviar")   

        if submitted: #Lançar os dados pra api autenticar
            url = 'https://rentup.up.railway.app/user/register'

            data = {
                "email": email,
                "password": password,
                "nome": nome,
                "contato": contato,
                "cargo": "USER",
            }
               
            response = requests.post(url, json=data) #Tratamnento de erros#
            
            if response.status_code == 201: #Se o usuário for logado com sucesso 
                st.session_state.cadastro = False
                st.rerun()
            elif response.status_code == 400:
                st.error('A solicitação de registro não atende aos requisitos')
            elif response.status_code == 409:
                st.error('Conflito de dados. O endereço de e-mail já está em uso por outro usuário.')
            else:
                st.error("Credenciais Inválidas")
                    

if 'cadastro' not in st.session_state:
    st.session_state.cadastro = False


if check_status(): # Se o usuário já estiver logado, o forms de login não aparecerá
   
    with st.sidebar:  #Definindo a sidebar global da interface do adm
        logo_container = st.container()
        
        with logo_container: 
            image = Image.open('img/logo.png')
            st.image(image, width=150, clamp=True)
            
        st.markdown("##")
        
        page = st.selectbox('Selecione uma página:', ('Dashboard', 'Inventário', 'Usuários', 'Empréstimos'))

        if st.button("Logout"): #Se o usuário deslogar, o arquivo json é removido e pede para fazer login novamente
            os.remove('auth_user')
            st.rerun()

    
    if page == 'Dashboard': #Redirecionando para a página escolhida
        dashboard.dashboard()
    elif page == 'Inventário':
        inventario.inventario()
    elif page == 'Usuários':
        usuarios.usuarios()
    elif page == 'Empréstimos':
        emprestimos.emprestimos()
        

else: # Enquanto o usuário não estiver logado, irá pedir para preencher o forms de  login
    
    if st.session_state.cadastro == False:
        login()  
    else:
        cadastro()
