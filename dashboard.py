import streamlit as st
from PIL import Image
import plotly.express as px
from api_permissions import get_token, check_status

def dashboard():
    with open('style.css') as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .mediumFont {
            font-size:18px !important;
            margin: 0px 0px 0em !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

        
    st.subheader('Dashboard', divider='orange')

    cols = st.columns([1,1,1])

    with cols[0]:
        st.markdown('<p class="mediumFont">Total de itens</p>', unsafe_allow_html=True)
        st.markdown('<p class="mediumFont">1234</p>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<p class="mediumFont">Itens danificados</p>', unsafe_allow_html=True)
        st.markdown('<p class="mediumFont">1234</p>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<p class="mediumFont">Empréstimos em andamento</p>', unsafe_allow_html=True)
        st.markdown('<p class="mediumFont">1234</p>', unsafe_allow_html=True)

    st.markdown("##")
    st.markdown("##")

    cols = st.columns([1, 1])

    with cols[0]:
        nomes = ['Aluno 1', 'Aluno 2', 'Aluno 3']
        email= ['aluno1@cesar.school', 'aluno2@cesar.school', 'aluno3@cesar.school']
        st.markdown('<p class="mediumFont">Empréstimos Recentes</p>', unsafe_allow_html=True)
        st.markdown("")
        df = {
            'Aluno': nomes,
            'Email': email,
        }
        
        st.dataframe(df,hide_index=True,)  # Same as st.write(df)
        
    with cols[1]:
        c1 = 2 
        c2 = 4 
        c3 = 6
        data = [c1, c2, c3]
        nomes = ['Componente 1', 'Componente 2', 'Componente 3']
        st.markdown('<p class="mediumFont">Mais Quebrados</p>', unsafe_allow_html=True)
        fig = px.pie(
            data,  
            values=data,
            names=nomes,
            color_discrete_sequence=px.colors.sequential.RdBu,
            height=300, width=200
        )
        
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)
        
        c1 = 20 
        c2 = 15 
        c3 = 10
        data = [c1, c2, c3]
        nomes = ['Componente 1', 'Componente 2', 'Componente 3']
        st.markdown('<p class="mediumFont">Mais Emprestados</p>', unsafe_allow_html=True)
        
        fig = px.pie(
            data,  
            values=data,
            names=nomes,
            color_discrete_sequence=px.colors.sequential.RdBu,
            height=300, width=200
        )
        
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)