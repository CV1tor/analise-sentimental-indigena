import pandas as pd
from LeIA import SentimentIntensityAnalyzer

def analisar_sentimento(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona score e agrega média por década."""
    sia = SentimentIntensityAnalyzer()
    df['score'] = df['texto'].apply(lambda t: sia.polarity_scores(str(t))['compound'])
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/processed/corpus.csv", encoding="utf-8")
    df = analisar_sentimento(df)
    df.to_csv("data/processed/corpus.csv", index=False, encoding="utf-8")
    print("Análise de sentimento concluída e corpus.csv atualizado.")
