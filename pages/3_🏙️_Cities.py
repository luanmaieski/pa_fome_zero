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
    st.title('🏙️ Visão Cidades')
    
with st.container():
    df_aux = df1.loc[:, ['city', 'restaurant_id']].groupby('city').count().sort_values(by='restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux, x='city', y='restaurant_id',
                 title='Cidades com mais restaurantes registrados',
                 labels={'city': 'Cidades', 'restaurant_id': 'Quantidade de restaurantes'}, 
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
    st.plotly_chart( fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[df1['aggregate_rating'] > 4, ['aggregate_rating', 'city']].groupby('city').count().sort_values(by='aggregate_rating', ascending=False).reset_index()
        fig = px.bar(df_aux, x='city', y='aggregate_rating', 
                     title='Cidades com mais restaurantes com nota maior que 4',
                     labels={'city': 'Cidades', 'aggregate_rating': 'Quantidade de restaurantes'},
                     color_discrete_sequence=px.colors.qualitative.D3)
        st.plotly_chart( fig, use_container_width=True)
    with col2:
        df_aux = df1.loc[df1['aggregate_rating'] < 2.5, ['aggregate_rating', 'city']].groupby('city').count().sort_values(by='aggregate_rating', ascending=False).reset_index()
        fig = px.bar(df_aux, x='city', y='aggregate_rating',
                     title='Cidades com mais restaurantes com nota menor que 2.5',
                     labels={'city': 'Cidades', 'aggregate_rating': 'Quantidade de restaurantes'},
                     color_discrete_sequence=px.colors.qualitative.G10)
        st.plotly_chart( fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[:, ['city', 'cuisines']].groupby('city').nunique().sort_values(by='cuisines', ascending=False).reset_index()
        fig = px.bar(df_aux, x='city', y='cuisines',
                     title='Cidades com mais tipos de culinária',
                     labels={'city': 'Cidades', 'cuisines': 'Quantidade de tipos de culinária'},
                     color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart( fig, use_container_width=True)
    
    with col2:
        df_aux = df1.loc[:, ['city', 'price_in_dollar']].groupby('city').mean().sort_values(by='price_in_dollar', ascending=False).reset_index()
        fig = px.bar(df_aux, x='city', y='price_in_dollar',
                     title='Cidades com maior valor médio de um prato para dois',
                     labels={'city': 'Cidades', 'price_in_dollar': 'Valor médio em dólar para prato para 2'},
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart( fig, use_container_width=True)