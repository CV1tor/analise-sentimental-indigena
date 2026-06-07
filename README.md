# 🪶 Representação Indígena no RN — Mineração de Texto e Análise de Sentimento

> Pipeline de coleta, processamento e visualização de textos históricos e jornalísticos para analisar como a figura do indígena norte-rio-grandense foi — e é — retratada na mídia e na historiografia local.

---

## 📌 Visão Geral

Este projeto aplica técnicas de **Processamento de Linguagem Natural (PLN)** sobre um corpus de textos extraídos de jornais históricos do Rio Grande do Norte (disponíveis na Hemeroteca Digital da Biblioteca Nacional) e de portais de notícias atuais do estado.

O sistema rastreia termos como `indígena`, `índio`, `potiguara`, `tapuia` e correlatos, gerando:

- Análise de frequência e contexto (KWIC)
- Nuvens de palavras por período histórico
- Classificação de sentimento ao longo do tempo
- Dashboard interativo e público

---

## 🎯 Objetivo do MVP (4 semanas)

Entregar uma **prova de conceito funcional e publicada** que demonstre o pipeline de ponta a ponta com um corpus inicial de 50 a 100 textos.

---

## 🗂️ Estrutura do Repositório

```
projeto-indigena-rn/
│
├── data/
│   ├── raw/              # Textos brutos coletados (imagens, TXTs, PDFs)
│   └── processed/        # corpus.csv — textos limpos e anotados
│
├── scripts/
│   ├── coleta.py         # Coleta e montagem do corpus
│   ├── limpeza.py        # Pré-processamento e limpeza
│   ├── frequencia.py     # Análise de frequência e nuvens
│   └── sentimento.py     # Classificação de sentimento
│
├── app/
│   └── dashboard.py      # App Streamlit (dashboard final)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Stack Tecnológica

### Instalação do ambiente

```bash
git clone https://github.com/seu-usuario/projeto-indigena-rn.git
cd projeto-indigena-rn

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt
python -m spacy download pt_core_news_lg
```

### Execução

As etapas são scripts Python independentes, executados em sequência no terminal:

```bash
python scripts/coleta.py
python scripts/limpeza.py
python scripts/frequencia.py
python scripts/sentimento.py
```

> **Sem Python instalado?** Use o [Google Colab](https://colab.research.google.com) — faça upload dos scripts e do `corpus.csv` e execute no navegador sem configuração local.

### `requirements.txt`

```
pandas
nltk
spacy
wordcloud
plotly
streamlit
easyocr
pytesseract
pillow
leia
openpyxl
```

---

## 🔄 Pipeline — Etapas

### Etapa · Coleta do Corpus

**Fonte principal:** [Hemeroteca Digital da Biblioteca Nacional](https://hemerotecadigital.bn.gov.br)

1. Acesse o site e busque pelos termos-alvo (`potiguara`, `índio`, `indígena`, `tapuia`)
2. Filtre por **Estado: Rio Grande do Norte** e selecione o período desejado
3. Para cada resultado, acesse o visualizador do jornal

**Como obter o texto:**

| Situação | O que fazer |
|---|---|
| OCR disponível no site | Clique em "Texto" ou "OCR" na barra lateral e copie o conteúdo |
| Apenas imagem disponível | Baixe o JPEG/PDF e rode o OCR localmente (ver abaixo) |
| Texto ilegível ou muito danificado | Transcreva manualmente apenas o parágrafo com o termo |

**Salve cada recorte no `corpus.csv`** com as colunas:

```
texto, fonte, ano, decada, url
```

---

### Etapa · Pré-processamento

Execute `scripts/limpeza.py`. O script realiza:

- Remoção de artefatos de OCR (hífens de quebra de linha, numeração de página)
- Normalização de acentuação e caixa
- Tokenização e remoção de stopwords (NLTK)
- Lematização com spaCy (`pt_core_news_lg`)

```python
import spacy, re
nlp = spacy.load("pt_core_news_lg")

def limpar(texto):
    texto = re.sub(r'-\n', '', texto)          # quebra de linha com hífen
    texto = re.sub(r'\s+', ' ', texto)         # espaços múltiplos
    texto = texto.lower().strip()
    doc = nlp(texto)
    tokens = [t.lemma_ for t in doc if not t.is_stop and t.is_alpha]
    return ' '.join(tokens)
```

---

### Etapa · Análise de Frequência e Nuvens

Execute `scripts/frequencia.py`.

```python
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Frequência geral
tokens = ' '.join(df['texto_limpo']).split()
freq = FreqDist(tokens)
freq.most_common(20)

# Nuvem por década
for decada, grupo in df.groupby('decada'):
    texto_unificado = ' '.join(grupo['texto_limpo'])
    nuvem = WordCloud(width=800, height=400, background_color='white').generate(texto_unificado)
    plt.title(f'Década de {decada}')
    plt.imshow(nuvem)
    plt.axis('off')
    plt.savefig(f'data/processed/nuvem_{decada}.png')
```

---

### Etapa · Análise de Sentimento

Execute `scripts/sentimento.py`.

```python
from leia import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
df['score'] = df['texto'].apply(lambda t: sia.polarity_scores(t)['compound'])

# Média de sentimento por década
serie = df.groupby('decada')['score'].mean().reset_index()
```

O score vai de **-1** (muito negativo) a **+1** (muito positivo). Valores próximos de zero indicam neutralidade ou ambiguidade.

---

### Etapa · Dashboard Streamlit

Execute localmente:

```bash
streamlit run app/dashboard.py
```

O dashboard possui três abas:

- **Nuvens** — nuvem de palavras filtrável por período
- **Sentimento** — gráfico de linha da evolução temporal
- **Explorador** — busca KWIC: mostra o contexto de cada menção ao termo

**Publicação gratuita:**

1. Suba o projeto no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório → Deploy

---

## 🔠 OCR — Alternativas quando o texto não está disponível

### Opção A · EasyOCR (recomendada para o MVP)

Não exige configuração adicional, funciona bem com português.

```python
import easyocr
reader = easyocr.Reader(['pt'])
resultado = reader.readtext('pagina.jpg', detail=0)
texto = ' '.join(resultado)
```

### Opção B · Tesseract

Melhor para páginas com tipografia clara e boa resolução.

```bash
sudo apt install tesseract-ocr tesseract-ocr-por
pip install pytesseract pillow
```

```python
from PIL import Image
import pytesseract

texto = pytesseract.image_to_string(Image.open('pagina.jpg'), lang='por')
```

### Opção C · API na nuvem (sem instalação)

Para equipes sem ambiente configurado, use uma API com camada gratuita:

| Serviço | Limite gratuito | Qualidade |
|---|---|---|
| Google Cloud Vision | 1.000 req/mês | ⭐⭐⭐⭐⭐ |
| Azure Document Intelligence | 500 pág/mês | ⭐⭐⭐⭐ |
| AWS Textract | 100 pág/mês | ⭐⭐⭐⭐ |

### Opção D · Transcrição manual

Para volumes pequenos (< 30 recortes), transcrever manualmente **apenas o parágrafo** com o termo é mais rápido do que configurar qualquer pipeline. Leva 3 a 5 minutos por recorte.

---

## 📊 Estrutura do `corpus.csv`

| Campo | Tipo | Exemplo |
|---|---|---|
| `texto` | string | "O gentio potiguara habitava..." |
| `fonte` | string | "A República" |
| `ano` | inteiro | 1923 |
| `decada` | inteiro | 1920 |
| `url` | string | https://hemerotecadigital.bn.gov.br/... |

---

## 🗓️ Cronograma MVP (4 semanas)

| Semana | Entregável |
|---|---|
| Corpus e ambiente | `corpus.csv` com 50–100 textos de ao menos 3 períodos distintos |
| Limpeza e frequência | Nuvens de palavras por década geradas e salvas |
| Sentimento | Gráfico de linha com evolução temporal do sentimento |
| Dashboard | App publicado no Streamlit Cloud com URL pública |

---

## 📚 Referências Bibliográficas Essenciais

**PLN e análise computacional**
- Jurafsky, D. & Martin, J.H. (2023). *Speech and Language Processing* — [online gratuito](https://web.stanford.edu/~jurafsky/slp3/)
- Souza, F. et al. (2020). BERTimbau: Pretrained BERT Models for Brazilian Portuguese. *BRACIS 2020*
- Hamilton, W. et al. (2016). Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change. *ACL 2016*
- Graham, S. et al. (2019). *Exploring Big Historical Data: The Historian's Macroscope*

**Representação indígena e identidade no RN**
- Hall, S. (org.) (1997). *Representation: Cultural Representations and Signifying Practices*. Sage
- Cascudo, L.C. (1955). *História do Rio Grande do Norte*. MEC
- Peres, E.T. (2013). *Sob o Pálio do Esquecimento*. EDUFRN
- Oliveira, J.P. (org.) (1999). *A Viagem da Volta*. Contra Capa

---

## 👥 Como a Equipe Deve Operar

| Papel | Responsabilidade |
|---|---|
| **Coleta** | Acessa a Hemeroteca, baixa os recortes e preenche o `corpus.csv` |
| **Processamento** | Executa os scripts em ordem, valida qualidade do OCR |
| **Visualização** | Mantém e evolui o `dashboard.py`, publica atualizações no Streamlit |
| **Curadoria** | Revisa anotações, identifica erros de OCR críticos, documenta decisões |

> **Convenção:** todo texto adicionado ao corpus deve ter `fonte`, `ano` e `url` preenchidos. Textos sem data definida usam `ano = 0` e `decada = 'indefinida'`.

---

*Projeto desenvolvido no contexto das Humanidades Digitais aplicadas ao estudo da identidade indígena no Rio Grande do Norte.*
