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