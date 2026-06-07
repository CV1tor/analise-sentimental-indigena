import re
import spacy
import pandas as pd

try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    import os
    os.system("python -m spacy download pt_core_news_lg")
    nlp = spacy.load("pt_core_news_lg")

def limpar(texto: str) -> str:
    """Normaliza texto histórico com OCR."""
    if not isinstance(texto, str): return ""
    texto = re.sub(r'-\n', '', texto)
    texto = re.sub(r'\s+', ' ', texto).lower().strip()
    doc = nlp(texto)
    return ' '.join(t.lemma_ for t in doc if not t.is_stop and t.is_alpha)

if __name__ == "__main__":
    df = pd.read_csv("data/processed/corpus.csv", encoding="utf-8")
    df['texto_limpo'] = df['texto'].apply(limpar)
    df.to_csv("data/processed/corpus.csv", index=False, encoding="utf-8")
    print("Limpeza concluída e corpus.csv atualizado.")
