import streamlit as st
from PIL import Image as img
import pandas as pd
import numpy as np


with open('style.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)
    

logo = img.open('img/logo.png')


with st.sidebar:
    st.image(logo, width= 200)
    st.markdown("##")
    st.text("Olá, Fulano!")
    st.divider()
    optionsContainer= st.container()
    with optionsContainer:
        st.button("Dashboard")
        st.button("Inventário")
        st.button("Empréstimos")
        st.button("Usuários Registrados")
 
       
searchBar_container = st.container()

col1, col2 = st.columns(2)


with searchBar_container:
    with col1:
        st.header("📦Inventário")
    with col2:
        searchInput = st.text_input("",placeholder="Buscar Item")


Addbutton_container = st.container()
with Addbutton_container:
    st.button("Adicionar Item")

st.markdown("##")

dataTable_container = st.container()
nomes = [f'Componente {i + 1}' for i in range(10)];

with dataTable_container:
   
    df =  {
    'Nome do Item': nomes,
    'Itens em Estoque': np.random.randint(10, 100, size=10),
    'Itens Danificados': np.random.randint(0, 10, size=10),
    'Itens Emprestados': np.random.randint(0, 10, size=10)
}
    
    st.dataframe(df,hide_index=True,)  # Same as st.write(df)
