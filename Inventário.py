import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

#streamlit run myfile.py
with open('style.css') as file:
    st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("##")
    st.text("Olá, Fulano!")


logo_container = st.container()
col1, col2, col3 = st.columns(3)

with logo_container:
    with col2:
        image = Image.open('img/logo.png')
        st.image(image, width=150)
 

    
st.subheader('Inventário', divider='orange')

searchBar_container = st.container()
col1, col2 = st.columns(2)
openForms = 0

with searchBar_container:
    with col1:
        searchInput = st.text_input("",placeholder="Buscar Item")
    with col2:
        
        if st.button("Adicionar Item"):
            openForms = 1
        #st.text(f'{x},{y}')

if openForms == 1:

    with st.form('form'):
        
        
        nome = st.text_input('Nome')
        quantidade = st.slider('Quantidade', 0, 100)
        categoria = st.selectbox('Categoria', ["categoria1", "categoria2", "categoria3"])

        col1, col2, col3 = st.columns(3)
        with col2:
            if st.form_submit_button('cancel'):
                st.warning('cancelled')

        with col3:
            if st.form_submit_button('submit'):
                st.success('updated successfully')


st.markdown("##")

dataTable_container = st.container()
nomes = [f'Componente {i + 1}' for i in range(10)];

with dataTable_container:
   
    df = {
        'Nome do Item': nomes,
        'Itens em Estoque': np.random.randint(10, 100, size=10),
        'Itens Danificados': np.random.randint(0, 10, size=10),
        'Itens Emprestados': np.random.randint(0, 10, size=10)
    }
    
    st.dataframe(df,hide_index=True,)  # Same as st.write(df)
