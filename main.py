import streamlit as st
from admPages import inventario, dashboard

# NAVEGAÇÃO PROVISÓRIA #
page = st.selectbox('Selecione uma página:', ('Inventário', 'Dashboard'), index = None)

if page == 'Inventário':
    inventario.inventario()

elif page == 'Dashboard':
    dashboard.dashboard()

