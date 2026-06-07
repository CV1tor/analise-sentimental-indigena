import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import glob
import os

st.set_page_config(page_title="Indígena no RN", layout="wide")

if os.path.exists('data/processed/corpus.csv'):
    df = pd.read_csv('data/processed/corpus.csv', encoding='utf-8')
else:
    st.error("Arquivo corpus.csv não encontrado.")
    st.stop()

aba_nuvem, aba_sentimento, aba_kwic = st.tabs(["Nuvens", "Sentimento", "Explorador"])

with aba_nuvem:
    decadas_disponiveis = sorted(df['decada'].unique())
    decada = st.select_slider("Período", options=decadas_disponiveis)
    imgs = glob.glob(f'data/processed/nuvem_{decada}.png')
    if imgs:
        st.image(Image.open(imgs[0]), use_container_width=True)
    else:
        st.warning(f"Nenhuma nuvem encontrada para a década {decada}. Rode scripts/frequencia.py primeiro.")

with aba_sentimento:
    if 'score' in df.columns:
        serie = df.groupby('decada')['score'].mean().reset_index()
        fig = px.line(serie, x='decada', y='score', markers=True,
                      labels={'decada': 'Década', 'score': 'Sentimento médio'})
        fig.add_hline(y=0, line_dash='dash', line_color='gray')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Coluna 'score' não encontrada. Rode scripts/sentimento.py primeiro.")

with aba_kwic:
    termo = st.text_input("Buscar termo", value="potiguara")
    resultado = df[df['texto'].str.contains(termo, case=False, na=False)]
    st.write(f"{len(resultado)} ocorrências encontradas")
    st.dataframe(resultado[['fonte', 'ano', 'texto']].head(30))
