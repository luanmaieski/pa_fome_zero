#Libraries
import pandas as pd
import streamlit as st
import inflection
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide', page_title='Países', page_icon='📊', initial_sidebar_state='expanded')

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

st.sidebar.markdown("""___""")

cuisines_select = st.sidebar.multiselect(
    'Selecione os tipos de culinária',
    df1.loc[:, 'cuisines'].unique().tolist(),
    default=['Italian', 'Japanese', 'Brazilian', 'Arabian', 'Home-made', 'American'])

st.sidebar.markdown("""___""")

#Filtro de Preço
linhas_selecionadas_min = df1['price_in_dollar'] >= price_min_slider
linhas_selecionadas_max = df1['price_in_dollar'] <= price_max_slider
df1 = df1.loc[linhas_selecionadas_max & linhas_selecionadas_min, :]

#Filtro de País
linhas_selecionadas = df1['country_name'].isin(country_select)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Culinária
linhas_selecionadas = df1['cuisines'].isin(cuisines_select)
df1 = df1.loc[linhas_selecionadas, :]


#=================================================
#Layout no Streamlit
#=================================================

with st.container():
    st.title('🌎 Visão Países')
    
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[:, ['country_name', 'city']].groupby('country_name').nunique().reset_index().sort_values(by='city', ascending=False)
        fig = px.bar(df_aux, x='country_name', y='city', 
                     title='Quantidade de Cidades registradas por País', 
                     labels={'country_name': 'País', 'city': 'Quantidade de Cidades'}, color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df_aux = df1.loc[:, ['country_name', 'restaurant_id']].groupby('country_name').nunique().reset_index().sort_values(by='restaurant_id', ascending=False)
        fig = px.bar(df_aux, x='country_name', y='restaurant_id',
                     title='       Quantidade de Restaurantes registradas por País',
                     labels={'country_name': 'País', 'restaurant_id': 'Quantidade de Restaurantes'}, color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[:, ['country_name', 'aggregate_rating']].groupby('country_name').mean().reset_index().sort_values(by='aggregate_rating', ascending=False)
        fig = px.bar(df_aux, x='country_name', y='aggregate_rating', 
                     title='Média de Avaliações por País',
                     labels={'country_name': 'País', 'aggregate_rating': 'Média de Avaliações'}, color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        df_aux = df1.loc[:, ['country_name', 'votes']].groupby('country_name').sum().reset_index().sort_values(by='votes', ascending=False)
        fig = px.bar(df_aux, x='country_name', y='votes', 
                     title='       Quantidade de Votos por País',
                     labels={'country_name': 'País', 'votes': 'Quantidade de Votos'}, color_discrete_sequence=[px.colors.qualitative.Dark24[0]])
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    df_aux = df1.loc[:, ['country_name', 'cuisines']].groupby('country_name').nunique().reset_index().sort_values(by='cuisines', ascending=False)
    fig = px.bar(df_aux, x='country_name', y='cuisines',
                 title='Países com maior quantidade de tipos de culinária distintos', 
                 labels={'country_name': 'País', 'cuisines': 'Quantidade de tipos de culinária'})
    st.plotly_chart(fig, use_container_width=True)
    