import pandas as pd
import re
from LeIA import SentimentIntensityAnalyzer

# Termos que devem ser ignorados no cálculo de sentimento (etnônimos e variantes)
TERMOS_INDIGENAS = [
    'índio', 'índia', 'índios', 'índias', 'indígena', 'indígenas', 
    'potiguara', 'potiguaras', 'tapuia', 'tapuias', 'gentio', 'gentios', 
    'nativo', 'nativos', 'silvícola', 'silvícolas', 'bugre', 'caboclo'
]

def extrair_contexto_focado(texto: str, janela: int = 20) -> str:
    """Extrai texto ao redor dos termos alvo e remove os próprios termos."""
    texto = str(texto)
    # Regex para encontrar os termos (case-insensitive)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, TERMOS_INDIGENAS)) + r')\b', re.IGNORECASE)
    
    # Se não encontrar nenhum termo, retorna o texto todo (mas limpo dos termos se houver)
    # ou podemos retornar o texto original sem os termos.
    # Vamos focar em remover os termos de qualquer forma para não enviesar.
    texto_sem_termos = pattern.sub('', texto)
    
    # Opcional: focar apenas em janelas se o texto for muito grande.
    # Para este projeto (fragmentos), remover os termos do texto completo já é eficaz.
    return texto_sem_termos

def analisar_sentimento_refinado(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o sentimento ignorando os termos identitários."""
    sia = SentimentIntensityAnalyzer()
    
    def calcular(texto):
        # 1. Remove os termos identitários antes da análise
        texto_focado = extrair_contexto_focado(texto)
        # 2. Calcula a polaridade do contexto restante
        return sia.polarity_scores(texto_focado)['compound']
    
    df['score'] = df['texto'].apply(calcular)
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/processed/corpus.csv", encoding="utf-8")
    df = analisar_sentimento_refinado(df)
    df.to_csv("data/processed/corpus.csv", index=False, encoding="utf-8")
    print("Análise de sentimento refinada concluída (etnônimos ignorados).")
