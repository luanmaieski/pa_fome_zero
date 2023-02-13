#Libraries
import pandas as pd
import streamlit as st
import inflection
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image

st.set_page_config(layout='wide', page_icon='📊', initial_sidebar_state='expanded')

#Import Dataset
df1 = pd.read_csv('dataset/dftratado.csv')
#df1 = df.copy()

#=================================================
#Barra lateral
#=================================================


image = Image.open('logo_restaurante.png')
col1, col2 = st.sidebar.columns([1, 2], gap='small')
col1.image(image, width=140)
col2.markdown('# Fome Zero')

st.sidebar.markdown("""___""")

price_min_slider, price_max_slider = st.sidebar.slider(
    ':heavy_dollar_sign: Preço para Dois',
    min_value=0,
    max_value=755, 
    value=[0, 755]
)

st.sidebar.markdown("""___""")

country_select = st.sidebar.multiselect(
    'Selecione os Países', 
    df1.loc[:, 'country_name'].unique().tolist(),
    default=['Brazil', "England", "Qatar", "South Africa", "Canada", "Australia", 'Turkey']
)

#Filtro de Preço
linhas_selecionadas_min = df1['price_in_dollar'] >= price_min_slider
linhas_selecionadas_max = df1['price_in_dollar'] <= price_max_slider
df1 = df1.loc[linhas_selecionadas_max & linhas_selecionadas_min, :]

#Filtro de País
linhas_selecionadas = df1['country_name'].isin(country_select)
df1 = df1.loc[linhas_selecionadas, :]


#=================================================
#Layout no Streamlit
#=================================================
st.title('Overall Metrics')
st.markdown("""___""")
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric('Restaurantes Cadastrados', value=df1['restaurant_id'].nunique(), help='Total de Restaurantes Cadastrados')
    
    with col2:
        st.metric('Países Cadastrados', value=df1['country_name'].nunique(), help= 'Total de Países Cadastrados')
        
    with col3:
        st.metric('Cidades Cadastradas', value=df1['city'].nunique(), help='Total de Cidades Cadastradas')
        
    with col4:
        st.metric('Avaliações Registradas', value=df1['votes'].sum(), help='Total de Avaliações Registradas')
        
    with col5:
        st.metric('Culinárias Registradas', value=df1['cuisines'].nunique(), help='Tipos de Culinárias Registradas')

st.markdown("""___""")

with st.container():
    locais = df1[['latitude', 'longitude']].values.tolist()
    mapa = folium.Map()
    markercluster = MarkerCluster().add_to(mapa)
    #MarkerCluster(locations=locais, popup=df1['restaurant_name']).add_to( mapa )
    for index, location_info in df1.iterrows():
        folium.Marker( [location_info['latitude'], location_info['longitude']], popup=location_info['restaurant_name'] ).add_to( markercluster )
    
    folium_static( mapa, width=1024, height=600)
    
    
    