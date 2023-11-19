import streamlit as st
from PIL import Image
import plotly.express as px
from api_permissions import get_token
import plotly.graph_objects as go
import json
import requests

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
        #st.write(data)
        
        with cols_up[0]:
            
            valores = [data["total_itens"]]
            
            df = {
                'Número de Itens' : valores    
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[1]:
            valores = [data["total_danificados"]]
            
            df = {
                'Itens Danificados' : valores
                
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[2]:
            valores = [data["total_emprestimos_andamento"]]
            
            df = {
                'Empréstimos em Andamento' : valores
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
    st.markdown("##")

    with st.container():
                
        nomes = ['Aluno 1', 'Aluno 2', 'Aluno 3']
        email= ['aluno1@cesar.school', 'aluno2@cesar.school', 'aluno3@cesar.school']
        
        st.markdown('<p class="mediumFont">Empréstimos Recentes</p>', unsafe_allow_html=True)
        st.markdown("")
        df = {
            'Aluno': nomes,
            'Email': email,
        }
        
        st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)

        
    with st.container():
        cols_down = st.columns([5, 0.5, 5])
        #st.write(data)
        
        with cols_down[0]:      
            
            colors = ['lightslategray',] * 3
            valores = [data["itens_mais_emprestados"][0]["qnt_emprestados"], data["itens_mais_emprestados"][1]["qnt_emprestados"], data["itens_mais_emprestados"][2]["qnt_emprestados"]]
            nomes = [item["nome"] for item in data["itens_mais_emprestados"]]
           

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
            
            colors = ['lightslategray',] * 3
            
            valores = [data["itens_mais_danificados"][0]["danificados"], data["itens_mais_danificados"][1]["danificados"], data["itens_mais_danificados"][2]["danificados"]]
            nomes = [item["nome"] for item in data["itens_mais_danificados"]]
            
            fig = go.Figure(
                data=[go.Bar(
                    x=nomes,
                    y=valores,
                    marker_color=colors # marker color can be a single color value or an iterable
            )])
            
            fig.update_layout(title_text='Itens Mais Danificados')
            st.plotly_chart(fig, use_container_width=True)
