# GEMINI.md — Agente: Mineração de Texto · Representação Indígena no RN

## CONTEXT

Projeto de PLN aplicado a corpus histórico-jornalístico do Rio Grande do Norte (Brasil).
Rastreia termos (`indígena`, `índio`, `potiguara`, `tapuia`) em jornais digitalizados (séc. XIX–XXI) e portais atuais.
Gera análise de frequência, nuvens de palavras, sentimento temporal e dashboard público.

**Stack:** Python 3.11 · pandas · NLTK · spaCy `pt_core_news_lg` · LeIA · WordCloud · Plotly · Streamlit
**Estrutura de dados central:** `data/processed/corpus.csv` → colunas: `texto, fonte, ano, decada, url`
**Scripts em:** `scripts/` → `coleta.py · limpeza.py · frequencia.py · sentimento.py`
**Dashboard:** `app/dashboard.py` → publicado no Streamlit Cloud

---

## RULES

### Comportamento geral
- Responda sempre em **português brasileiro**
- Seja direto e objetivo; evite explicações redundantes
- Ao sugerir código, use apenas as bibliotecas já declaradas no `requirements.txt`
- Nunca proponha refatoração de arquivos que não foram explicitamente mencionados na tarefa
- Se a tarefa for ambígua, faça **uma única pergunta** de esclarecimento antes de executar

### Código
- Siga PEP8; funções com docstring de uma linha
- Variáveis e comentários em **português**
- Scripts devem ser executáveis independentemente (`if __name__ == "__main__":`)
- Leitura/escrita de arquivos sempre com `encoding="utf-8"`
- Erros de OCR são esperados — nunca trate ausência de texto como exceção fatal; use fallback silencioso com log

### Dados
- O `corpus.csv` é a única fonte de verdade; nunca sobrescreva sem backup (`corpus_backup.csv`)
- Textos sem data definida: `ano = 0`, `decada = "indefinida"`
- Campos obrigatórios ao inserir linha: `texto`, `fonte`, `ano` — os demais podem ser vazios
- Sentimento é calculado pelo LeIA (`compound`); escala de -1 a +1

### Limites
- Não sugira modelos que exijam GPU sem avisar o custo computacional
- Não use `selenium` ou `playwright` no MVP — coleta é manual ou via EasyOCR
- Não conecte a APIs externas pagas sem confirmar com o usuário
- Não altere o `dashboard.py` sem rodar `streamlit run app/dashboard.py` localmente antes

---

## SKILLS

### SKILL · Limpeza de texto histórico
Aplica pipeline de normalização em textos com OCR imperfeito.

```python
import re, spacy
nlp = spacy.load("pt_core_news_lg")

def limpar(texto: str) -> str:
    """Normaliza texto histórico com OCR."""
    texto = re.sub(r'-\n', '', texto)
    texto = re.sub(r'\s+', ' ', texto).lower().strip()
    doc = nlp(texto)
    return ' '.join(t.lemma_ for t in doc if not t.is_stop and t.is_alpha)
```

**Quando usar:** sempre antes de qualquer análise; entrada = coluna `texto`; saída = coluna `texto_limpo`.

---

### SKILL · OCR de imagem
Extrai texto de imagens de jornais quando o OCR do site não está disponível.

```python
# Opção A — EasyOCR (padrão do projeto)
import easyocr
def ocr_imagem(caminho: str) -> str:
    """Extrai texto de imagem via EasyOCR."""
    reader = easyocr.Reader(['pt'], gpu=False)
    return ' '.join(reader.readtext(caminho, detail=0))

# Opção B — Tesseract (tipografia clara, boa resolução)
from PIL import Image
import pytesseract
def ocr_tesseract(caminho: str) -> str:
    """Extrai texto via Tesseract."""
    return pytesseract.image_to_string(Image.open(caminho), lang='por')
```

**Quando usar:** arquivo em `data/raw/` sem texto associado. Priorize EasyOCR; use Tesseract se EasyOCR retornar < 20 tokens.

---

### SKILL · Análise de frequência e KWIC
Conta ocorrências e extrai contexto ao redor dos termos-alvo.

```python
from nltk import FreqDist, word_tokenize

TERMOS = ['indígena', 'índio', 'potiguara', 'tapuia']

def frequencia(textos: list[str]) -> FreqDist:
    """Retorna distribuição de frequência do corpus."""
    tokens = [t for texto in textos for t in word_tokenize(texto, language='portuguese')]
    return FreqDist(tokens)

def kwic(texto: str, termo: str, janela: int = 150) -> list[str]:
    """Retorna janelas de contexto ao redor do termo."""
    import re
    return re.findall(rf'.{{0,{janela}}}{termo}.{{0,{janela}}}', texto, re.IGNORECASE)
```

**Quando usar:** após limpeza; resultado alimenta nuvens e o explorador KWIC do dashboard.

---

### SKILL · Análise de sentimento
Classifica polaridade de cada texto e agrega por período.

```python
import pandas as pd
from leia import SentimentIntensityAnalyzer

def analisar_sentimento(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona score e agrega média por década."""
    sia = SentimentIntensityAnalyzer()
    df['score'] = df['texto'].apply(lambda t: sia.polarity_scores(t)['compound'])
    return df

def serie_temporal(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna média de sentimento por década."""
    return df.groupby('decada')['score'].mean().reset_index()
```

**Quando usar:** após limpeza; `score` entre -1 (negativo) e +1 (positivo); agregar com `serie_temporal()` para o gráfico de linha.

---

### SKILL · Nuvem de palavras por período
Gera e salva imagem de nuvem para cada década do corpus.

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def nuvem_por_decada(df, coluna='texto_limpo', saida='data/processed/'):
    """Gera nuvem de palavras por década e salva em PNG."""
    for decada, grupo in df.groupby('decada'):
        texto = ' '.join(grupo[coluna].dropna())
        nuvem = WordCloud(width=800, height=400, background_color='white',
                          colormap='copper').generate(texto)
        plt.figure(figsize=(10, 5))
        plt.imshow(nuvem, interpolation='bilinear')
        plt.axis('off')
        plt.title(str(decada), fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{saida}nuvem_{decada}.png', dpi=150)
        plt.close()
```

**Quando usar:** após limpeza; arquivos salvos em `data/processed/`; carregados pelo dashboard.

---

### SKILL · Dashboard Streamlit
Estrutura mínima do app com três abas.

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import glob

st.set_page_config(page_title="Indígena no RN", layout="wide")
df = pd.read_csv('data/processed/corpus.csv', encoding='utf-8')

aba_nuvem, aba_sentimento, aba_kwic = st.tabs(["Nuvens", "Sentimento", "Explorador"])

with aba_nuvem:
    decada = st.select_slider("Período", options=sorted(df['decada'].unique()))
    imgs = glob.glob(f'data/processed/nuvem_{decada}.png')
    if imgs:
        st.image(Image.open(imgs[0]), use_column_width=True)

with aba_sentimento:
    serie = df.groupby('decada')['score'].mean().reset_index()
    fig = px.line(serie, x='decada', y='score', markers=True,
                  labels={'decada': 'Década', 'score': 'Sentimento médio'})
    fig.add_hline(y=0, line_dash='dash', line_color='gray')
    st.plotly_chart(fig, use_container_width=True)

with aba_kwic:
    termo = st.text_input("Buscar termo", value="potiguara")
    resultado = df[df['texto'].str.contains(termo, case=False, na=False)]
    st.write(f"{len(resultado)} ocorrências encontradas")
    st.dataframe(resultado[['fonte', 'ano', 'texto']].head(30))
```

**Quando usar:** etapa final; executar com `streamlit run app/dashboard.py`; publicar via Streamlit Cloud conectando o repositório GitHub.

---

## FLUXO DE EXECUÇÃO

```
coleta manual (Hemeroteca / EasyOCR)
        ↓
   corpus.csv
        ↓
  scripts/limpeza.py      →  coluna texto_limpo
        ↓
  scripts/frequencia.py   →  nuvens PNG em data/processed/
        ↓
  scripts/sentimento.py   →  coluna score + série temporal
        ↓
  app/dashboard.py        →  streamlit run → publicar
```

---

## REFERÊNCIAS RÁPIDAS

| Necessidade | Solução |
|---|---|
| OCR indisponível | EasyOCR → Tesseract → transcrição manual |
| Sem Python local | Google Colab |
| Publicação | Streamlit Cloud (gratuito) |
| Corpus insuficiente | Expandir busca na Hemeroteca por sinônimos e variantes |
| Sentimento impreciso | Anotar 200+ exemplos e fazer fine-tuning do BERTimbau |
