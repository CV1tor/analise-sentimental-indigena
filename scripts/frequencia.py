import pandas as pd
from nltk import FreqDist, word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

def gerar_nuvem_por_decada(df, coluna='texto_limpo', saida='data/processed/'):
    """Gera nuvem de palavras por década e salva em PNG."""
    for decada, grupo in df.groupby('decada'):
        texto = ' '.join(grupo[coluna].astype(str).dropna())
        if not texto.strip(): continue
        nuvem = WordCloud(width=800, height=400, background_color='white',
                          colormap='copper').generate(texto)
        plt.figure(figsize=(10, 5))
        plt.imshow(nuvem, interpolation='bilinear')
        plt.axis('off')
        plt.title(str(decada), fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{saida}nuvem_{decada}.png', dpi=150)
        plt.close()
        print(f"Nuvem da década {decada} salva.")

if __name__ == "__main__":
    df = pd.read_csv("data/processed/corpus.csv", encoding="utf-8")
    gerar_nuvem_por_decada(df)
