import pandas as pd
from nltk import FreqDist, word_tokenize
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

# Termos que devem ser ignorados nas nuvens de palavras (etnônimos e variantes)
TERMOS_INDIGENAS = [
    'índio', 'índia', 'índios', 'índias', 'indígena', 'indígenas', 
    'potiguara', 'potiguaras', 'tapuia', 'tapuias', 'gentio', 'gentios', 
    'nativo', 'nativos', 'silvícola', 'silvícolas', 'bugre', 'caboclo',
    'povo', 'povos', 'homem', 'mulher', 'gente', 'terra'
]

def gerar_nuvem_por_decada(df, coluna='texto_limpo', saida='data/processed/'):
    """Gera nuvem de palavras por década e salva em PNG."""
    # Amplia as stopwords com os termos indígenas
    stopwords = set(STOPWORDS)
    stopwords.update(TERMOS_INDIGENAS)
    
    for decada, grupo in df.groupby('decada'):
        texto = ' '.join(grupo[coluna].astype(str).dropna())
        if not texto.strip(): continue
        
        nuvem = WordCloud(width=800, height=400, 
                          background_color='white',
                          colormap='copper',
                          stopwords=stopwords).generate(texto)
        
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
