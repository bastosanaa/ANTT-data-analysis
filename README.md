# Railway Network Monitoring Dashboard (ANTT)

Dashboard interativo para monitoramento da malha ferroviária brasileira baseado na Declaração de Rede 2025 da ANTT (Agência Nacional de Transportes Terrestres).

## 📋 Descrição do Projeto

Este projeto implementa um pipeline ETL (Extract, Transform, Load) em Python com PySpark e uma dashboard interativa com Streamlit para análise de indicadores operacionais da malha ferroviária, como:

- **Licenciamento de pátios** por situação operacional
- **Tempo médio de licenciamento** por corredor/linha
- **Identificação de corredores congestionados**
- **Análise da dispersão** de tempos de processamento

## 🏗️ Arquitetura do Projeto

```
├── app.py                    # Dashboard Streamlit
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
└── db/
    ├── etl.py               # Orquestrador do pipeline ETL
    ├── extract.py           # Extração de dados do Excel
    ├── transform.py         # Transformação com PySpark
    ├── load.py              # Carregamento no banco SQLite
    └── data/
        ├── temp/            # Arquivos CSV temporários
        └── antt.db          # Banco de dados SQLite (gerado)
```

## 🚀 Como Começar

### 1. Pré-requisitos

- Python 3.11-


### 2. Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o Pipeline ETL

O ETL extrai dados do Excel, transforma com PySpark e carrega no SQLite:

```bash
python db\etl.py
```

**O que acontece:**
- ✅ Extrai abas do Excel (`DR2025-MRS.xlsx`)
- ✅ Exporta para CSV em `db/data/temp/`
- ✅ Transforma os dados com PySpark
- ✅ Cria tabelas normalizadas em `db/data/antt.db`

### 5. Iniciar o Dashboard

```bash
streamlit run app.py
```

O dashboard abrirá em `http://localhost:8501`

## 🛠️ Estrutura de Arquivos

### `app.py`
Dashboard principal em Streamlit. Interface interativa para explorar dados do banco SQLite.

### `db/etl.py`
Orquestrador do pipeline. Coordena extração, transformação e carregamento dos dados.

### `db/extract.py`
Extrai abas do Excel (`Pátios`, `Terminais`, `Entre Pátios`, `Entre Trechos`) e exporta como CSV.

### `db/transform.py`
Aplica transformações com PySpark:
- Limpeza de dados (valores nulos, tipos de dado)
- Normalização de colunas
- Cálculo de métricas

### `db/load.py`
Modela dados e carrega no SQLite:
- Cria tabelas dimensionais (`dim_linhas`)
- Cria tabelas de fatos (`patios`)
- Configura índices e relacionamentos

## 📦 Dependências Principais

| Pacote | Versão | Função |
|--------|--------|--------|
| `streamlit` | ~1.28 | Dashboard web |
| `pandas` | ~2.0 | Manipulação de dados |
| `pyspark` | ~3.5 | Processamento distribuído |
| `openpyxl` | ~3.1 | Leitura de Excel |
| `plotly` | ~5.0 | Gráficos interativos |
| `sqlite3` | Built-in | Banco de dados |

Para instalar todas: `pip install -r requirements.txt`

## 🔧 Configuração

### Variáveis de Ambiente

A aplicação usa caminhos relativos e espera a seguinte estrutura:

```
db/
  data/
    DR2025-MRS.xlsx    ← Arquivo Excel com dados de entrada
    temp/              ← CSVs temporários
    antt.db            ← Banco de dados SQLite (criado pelo ETL)
```

## 📈 Fluxo de Dados

```
DR2025-MRS.xlsx
    ↓
[Extract] → CSV files (temp/)
    ↓
[Transform] → PySpark (limpeza, validação)
    ↓
[Load] → SQLite (antt.db)
    ↓
[Dashboard] → Visualização em Streamlit
```

