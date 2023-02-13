#Libraries
import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config( page_title="Home", page_icon="📌", layout='wide' )


#Import Dataset
df1 = pd.read_csv('dataset/dftratado.csv')

#Barra lateral
image = Image.open('logo_restaurante.png')
col1, col2 = st.sidebar.columns([1, 2], gap='small')
col1.image(image, width=140)
col2.markdown('# Fome Zero')

st.sidebar.markdown("""___""")

country_select = st.sidebar.multiselect(
    'Selecione os Países', 
    df1.loc[:, 'country_name'].unique().tolist(),
    default=['Brazil', "England", "Qatar", "South Africa", "Canada", "Australia", 'Turkey']
)

#Filtro de País
linhas_selecionadas = df1['country_name'].isin(country_select)
df1 = df1.loc[linhas_selecionadas, :]

st.sidebar.markdown("""___""")

@st.cache
def convert_df(df1):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df1.to_csv().encode('utf-8')

csv = convert_df(df1)

st.sidebar.markdown("Base de dados tratada")
st.sidebar.download_button(label='Download', data=csv, file_name='dftratado.csv', mime='text/csv')
st.sidebar.markdown("""___""")

st.write('# Fome Zero Growth Dashboard')
st.markdown(
    """
    Este Dashboard foi construído para acompanhar as métricas de crescimento dos restaurantes e tipos de culinária com base na localização.
    ### O dashboard está divido em 4 visões:
    - General: métricas gerais e a localização dos restaurantes no mapa;
    - Country: análises de métricas por País;
    - Cities: análise das métricas por Cidade;
    - Cuisines: informação sobre os restaurantes e tipos de culinária.
    
    
    ### Ask for Help
    - Time de Data Science no Discord
        - @luan
    """)


