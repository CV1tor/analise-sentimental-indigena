# Representação Indígena no RN: Mineração de Texto e História

Este projeto utiliza técnicas de Processamento de Linguagem Natural (PLN) para analisar a representação dos povos indígenas (Potiguara, Tapuia, etc.) em textos históricos, documentos coloniais e notícias contemporâneas do Rio Grande do Norte.

## 📊 O Projeto
O objetivo é rastrear a evolução do sentimento e dos termos associados à temática indígena ao longo de três períodos fundamentais:
- **1500 – 1600:** Relatos de cronistas e primeiros contatos (Literatura de Informação).
- **1700 – 1800:** Conflitos coloniais, aldeamentos e resistência (Guerra dos Bárbaros).
- **1900 – 2000:** Século XX, atuação do SPI/FUNAI e reemergência étnica.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.14+
- **Processamento de Texto:** spaCy (`pt_core_news_lg`), NLTK
- **Análise de Sentimento:** LeIA (Léxico para Inferência Adaptada)
- **Visualização:** WordCloud, Plotly, Streamlit
- **Dados:** Pandas

## 📁 Estrutura de Arquivos
- `data/processed/corpus.csv`: Base de dados central com 150 textos reais.
- `scripts/limpeza.py`: Normalização e lematização dos textos.
- `scripts/sentimento.py`: Cálculo de polaridade (-1 a +1).
- `scripts/frequencia.py`: Geração de nuvens de palavras por década.
- `app/dashboard.py`: Dashboard interativo.

## 🚀 Como Rodar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/historia-indigena.git
cd historia-indigena
```

### 2. Configurar o ambiente virtual
```powershell
# No Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_lg
```

### 4. Executar o Pipeline (Opcional se já houver dados processados)
```powershell
python scripts/limpeza.py
python scripts/sentimento.py
python scripts/frequencia.py
```

### 5. Iniciar o Dashboard
```bash
streamlit run app/dashboard.py
```

## 🌐 Deploy
O dashboard pode ser acessado online via Streamlit Cloud:
*(Link será inserido após o deploy)*

---
**Desenvolvido como ferramenta de pesquisa histórica e linguística.**
