import streamlit as st
from PIL import Image
import plotly.express as px
from api_permissions import get_token
import plotly.graph_objects as go
import json
import requests
import pandas as pd

def dashboard():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .mediumFont {
            font-size:16px !important;
            font-weight: bold; !important
            margin: 0px 0px 0em !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

        
    st.subheader('Dashboard', divider='orange')

    with st.container():
        cols_up = st.columns([1, 1, 1])
        
        response = requests.get("https://rentup.up.railway.app/data/dashboard", headers=headers)
        data = json.loads(response.text)
        
        with cols_up[0]:
            
            valores_itens = [data["total_itens"]]
            
            df = {
                'Número de Itens' : valores_itens
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[1]:
            valores_danificados = [data["total_danificados"]]
            
            df = {
                'Itens Danificados' : valores_danificados
                
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[2]:
            valores_emprestimos = [data["total_emprestimos_andamento"]]
    
            df = {
                'Empréstimos em Andamento' : valores_emprestimos
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
    st.markdown("##")

    ##Tabela de aprovação de empréstimos
    with st.container():
        if 'aprovar' not in st.session_state:
            st.session_state.aprovar = False
        
        cols_down = st.columns([6.5, 1,1.5])
        with cols_down[0]:
            st.markdown('<p class="mediumFont">Solicitações de Empréstimo</p>', unsafe_allow_html=True)
        with cols_down[2]:
           if st.button("Aprovar", type='secondary', use_container_width=True):
               st.session_state.aprovar = True
       
        if st.session_state.aprovar:
            with st.form("Aprovar", True):
                st.write("Aprovar Solicitação")

                id_emprestimo = st.text_input('ID do Empréstimo')
                novo_status = st.selectbox('Novo Status:', ('APROVED', 'DISAPROVED'))

                cols = st.columns([5.5,1,0.8])
                with cols[1]:
                    calcelar = st.form_submit_button("Cancelar")
                with cols[2]:
                    submitted = st.form_submit_button("Enviar")

                if submitted:
                    response = requests.put(f"https://rentup.up.railway.app/rent/update-status?id_rent={id_emprestimo}&stat={novo_status}", headers=headers)

                    if response.status_code == 200:
                        st.session_state.aprovar = False
                        st.toast("Solicitação Aprovada")
                        st.rerun()
                    elif response.status_code == 401:
                        st.toast("Não autorizado")
                    elif response.status_code == 403:
                        st.toast("Não autorizado")
                    elif response.status_code == 404:
                        st.toast("Nenhum empréstimo com o ID especificado foi encontrado no sistema")   
                if calcelar:
                    st.session_state.aprovar = False
                    st.rerun()   

     
        response = requests.get("https://rentup.up.railway.app/rent/history", headers=headers)
        data = json.loads(response.text)

        df = pd.DataFrame(data)

        df_update = df[df['estado'] == 'WAITING']
        df_update.columns = ['ID', 'Usuário', 'Item', 'Data do Empréstimo', 'Data da Devolução', 'Status']
        df_update = df_update.drop(columns=['Data da Devolução'])

        st.dataframe(df_update,hide_index=True, use_container_width=True)  # Same as st.write(df)

        
    with st.container():
        response = requests.get("https://rentup.up.railway.app/data/dashboard", headers=headers)
        data = json.loads(response.text)

        cols_down = st.columns([5, 0.5, 5])
        
        with cols_down[0]:      
            num_itens = len(data["itens_mais_emprestados"])

            colors = ['lightslategray',] * 3
            valores = [item["qnt_emprestados"] for item in data["itens_mais_emprestados"]][:num_itens]
            nomes = [item["nome"] for item in data["itens_mais_emprestados"]][:num_itens]
           

            # Criar a figura
            fig = go.Figure(data=[go.Bar(
                x=nomes,
                y=valores,
                marker_color=colors # Cor do marcador pode ser um valor único ou um iterável
            )])
            
            fig.update_layout(title_text='Itens Mais Emprestados')
            st.plotly_chart(fig, use_container_width=True)

            
        with cols_down[2]:
            #st.markdown('<p class="mediumFont">Mais Emprestados</p>', unsafe_allow_html=True)
            num_itens = len(data["itens_mais_danificados"])
            colors = ['lightslategray',] * 3
            valores = [item["danificados"] for item in data["itens_mais_danificados"]][:num_itens]
            nomes = [item["nome"] for item in data["itens_mais_danificados"]][:num_itens]

    
            
            fig = go.Figure(
                data=[go.Bar(
                    x=nomes,
                    y=valores,
                    marker_color=colors # marker color can be a single color value or an iterable
            )])
            
            fig.update_layout(title_text='Itens Mais Danificados')
            st.plotly_chart(fig, use_container_width=True)