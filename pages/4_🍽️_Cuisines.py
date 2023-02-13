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
    st.title('🍽️ Visão Tipos de Culiária')
    st.title('Melhores restaurantes dos principais tipos de culinária')

with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        df_aux = df1.loc[df1['cuisines'] == 'Italian', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='Italian', value=' ', delta=df_aux, delta_color='off')
        
    with col2:
        df_aux = df1.loc[df1['cuisines'] == 'American', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='American', value=' ', delta=df_aux, delta_color='off')
        
    with col3:
        df_aux = df1.loc[df1['cuisines'] == 'Arabian', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='Arabian', value=' ', delta=df_aux, delta_color='off')
        
    with col4:
        df_aux = df1.loc[df1['cuisines'] == 'Japanese', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='Japanese', value=' ', delta=df_aux, delta_color='off')
        
    with col5:
        df_aux = df1.loc[df1['cuisines'] == 'Home-made', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='Home-made', value=' ', delta=df_aux)
        
    with col6:
        df_aux = df1.loc[df1['cuisines'] == 'Brazilian', ['restaurant_name', 'aggregate_rating', 'restaurant_id']].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0, 0]
        st.metric(label='Brazilian', value='  ' , delta=df_aux, delta_color='off')
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[:, ['cuisines', 'price_in_dollar']].groupby('cuisines').mean().round(2).sort_values(by='price_in_dollar', ascending=False).reset_index().head(10)
        fig = px.bar( df_aux, x='cuisines', y='price_in_dollar',
                      title='Top 10 culinária com maior valor médio para dois',
                      labels={'cuisines': 'Culinária', 'price_in_dollar': 'Valor em Dólar'},
                      color_discrete_sequence=px.colors.qualitative.Vivid,
                      color='cuisines')
        st.plotly_chart(fig, use_conteiner_width=True)
        
    with col2:
        df_aux = df1.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating', ascending=False).reset_index().head(10)
        fig = px.bar( df_aux, x='cuisines', y='aggregate_rating',
                      title='Top 10 tipos de Culinária',
                      labels={'cuisines': 'Culinária', 'aggregate_rating': 'Média das Avaliações médias'},
                      color_discrete_sequence=px.colors.qualitative.G10,
                      color='cuisines')
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1.loc[:, ['restaurant_name', 'price_in_dollar']].groupby('restaurant_name').max().sort_values(by='price_in_dollar', ascending=False).reset_index().head(10)
        fig = px.bar(df_aux, x='restaurant_name', y='price_in_dollar',
                     title='Top 10 restaurantes com maior valor médio para dois',
                     labels={'restaurant_name': 'Nome do Restaurante', 'price_in_dollar': 'Valor em Dólar'},
                     color_discrete_sequence=px.colors.qualitative.G10)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        df_aux = df1.loc[:, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating', ascending=False).reset_index().head(10)
        fig = px.bar(df_aux, x='restaurant_name', y='aggregate_rating',
                     title='Top 10 restaurantes com maior nota Média',
                     labels={'restaurant_name': 'Nome do Restaurante', 'aggregate_rating': 'Nota Média'},
                     color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig, use_container_width=True)
