import streamlit as st
from PIL import Image
import plotly.express as px
from api_permissions import get_token
import plotly.graph_objects as go

def dashboard():
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
        
        with cols_up[0]:
            valores = ['345']
            df = {
                'Número de Itens' : valores
                
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[1]:
            valores = ['20']
            
            df = {
                'Itens Danificados' : valores
                
            }
            
            st.dataframe(df,hide_index=True, use_container_width=True)  # Same as st.write(df)
            
        with cols_up[2]:
            valores = ['15']
            
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

        with cols_down[0]:
            
            colors = ['lightslategray',] * 5

            fig = go.Figure(data=[go.Bar(
                x=['Arduíno', 'Arduíno Nano', 'Protoboard', 'Jumper'],
                y=[20, 14, 23, 25],
                marker_color=colors # marker color can be a single color value or an iterable
            )])
            fig.update_layout(title_text='Itens Mais Emprestados')
            st.plotly_chart(fig, use_container_width=True)

            
        with cols_down[2]:
            #st.markdown('<p class="mediumFont">Mais Emprestados</p>', unsafe_allow_html=True)
            
            colors = ['lightslategray',] * 5

            fig = go.Figure(
                data=[go.Bar(
                    x=['Arduíno', 'Arduíno Nano', 'Protoboard', 'Jumper'],
                    y=[20, 14, 23, 25],
                    marker_color=colors # marker color can be a single color value or an iterable
            )])
            
            fig.update_layout(title_text='Itens Mais Danificados')
            st.plotly_chart(fig, use_container_width=True)
