# 🚆 Dashboard ANTT - Declaração de Rede Ferroviária

Acesse o dashboard:
[Deployed application ](https://antt-data-analysis.streamlit.app/)

> **Desafio Técnico**: Engenharia de Dados e Visualização Interativa com Python

Um dashboard para análise da infraestrutura ferroviária brasileira, desenvolvido como parte de um desafio técnico que avalia habilidades em ETL, modelagem de dados e desenvolvimento de painéis interativos.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**[🇺🇸 Read in English](#-english-version)**

---

## 📋 Sobre o Desafio

Este projeto foi desenvolvido como resposta a um desafio técnico que simula um cenário real de engenharia de dados. O objetivo é demonstrar competências em:

- **Ingestão de Dados**: Extração de múltiplas fontes (CSV, Excel)
- **Modelagem Relacional**: Estruturação de banco de dados SQLite com relacionamentos
- **ETL Pipeline**: Processo completo de extração, transformação e carga
- **Visualização de Dados**: Dashboard interativo com insights acionáveis
- **Arquitetura de Software**: Código modular, escalável e bem documentado

### 🎯 Requisitos Técnicos Atendidos

✅ Ingestão de **3+ conjuntos de dados** da Declaração de Rede (ANTT)  
✅ Modelagem relacional com **chaves e relacionamentos** coerentes  
✅ Dashboard com **3+ seções interativas** e navegação lateral  
✅ Gráficos interativos usando **Plotly**  
✅ Código estruturado e **documentado**  
✅ Repositório Git com **README completo**  
✅ Aplicação executável com `streamlit run app.py`  

### 📊 Análises Disponíveis

#### 1️⃣ Licenciamento de Pátios
- Impacto da situação operacional nos tempos de licenciamento
- Identificação de corredores congestionados
- Análise de dispersão por linha ferroviária

#### 2️⃣ Capacidade de Terminais
- Distribuição de capacidade por tipo de mercadoria
- Classificação automática por setor (Mineração, Agrícola, Construção)
- Ranking dos maiores terminais
- Visualização em treemap e gráficos de pizza

#### 3️⃣ Relação Carga vs. Velocidade
- Trade-off físico entre peso e velocidade autorizada (VMA)
- Análise de velocidade comercial (VMC)
- Auditoria de consistência de dados (VMC > VMA)
- Ranking de eficiência operacional por corredor

## 🏗️ Arquitetura do Projeto

```
antt-railway-dashboard/
│
├── app.py                          # Entry point do dashboard
├── run_etl.py                      # Entry point do pipeline ETL
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── .gitignore
│
├── config/                         # Configurações centralizadas
│   ├── settings.py                # Config do dashboard
│   ├── translations.py            # Sistema i18n (PT/EN)
│   └── etl_config.py              # Config do pipeline ETL
│
├── etl/                            # Pipeline ETL
│   ├── __init__.py
│   ├── extract.py                 # Extração de dados brutos
│   ├── transform.py               # Limpeza e transformação
│   ├── load.py                    # Carregamento no SQLite
│   ├── validators.py              # Validações de qualidade
│   └── utils.py                   # Funções auxiliares
│
├── src/                            # Módulos do Dashboard
│   ├── database/
│   │   └── queries.py             # Queries SQL organizadas
│   ├── data/
│   │   └── loader.py              # Carregamento com cache
│   ├── utils/
│   │   └── helpers.py             # Funções auxiliares
│   └── pages/
│       ├── page_yards.py          # Página: Pátios
│       ├── page_capacity.py       # Página: Capacidade
│       └── page_speed.py          # Página: Velocidade
│
├── data/                           # Dados brutos (não versionados)
│   ├── raw/                       # CSV/Excel originais da ANTT
│   └── processed/                 # Dados processados
│
└── db/
    └── data/
        └── antt.db                # Banco SQLite (gerado pelo ETL)
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11
- Java JDK (Obrigatório para o PySpark processar os dados)
- pip (gerenciador de pacotes Python)

### 1. Configuração do Ambiente (Windows)

Antes de instalar as dependências, é recomendável criar um ambiente virtual isolado. No terminal (PowerShell), execute:

```powershell
# 1.1 Crie o ambiente virtual
python -m venv venv

# 1.2 Ative o ambiente
.\venv\Scripts\activate

# 1.3 Configure o JAVA_HOME (Essencial para o PySpark)
# Nota: Verifique se o caminho abaixo corresponde à sua instalação do Java
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o Pipeline ETL
```bash
python ./db/etl.py
```
> Este comando irá:
> - Extrair dados dos arquivos CSV/Excel
> - Limpar e transformar os dados
> - Criar o banco de dados SQLite em `db/data/antt.db`

### 4. Execute o Dashboard
```bash
streamlit run app.py
```

### 5. Acesse no Navegador
```
http://localhost:8501
```

## 📊 Modelo de Dados

### Tabelas Principais

**Tabelas Fato:**
- `patios` - Pátios ferroviários (tempo de licenciamento, localização)
- `terminais` - Terminais de carga (capacidade por mercadoria)
- `trechos_fisicos` - Segmentos de via (carga máxima, velocidades)

**Tabelas Dimensão:**
- `dim_linhas` - Linhas/corredores ferroviários
- `dim_mercadorias` - Tipos de mercadorias transportadas

### Relacionamentos
```
patios.id_linha → dim_linhas.id_linha
terminais.id_mercadoria → dim_mercadorias.id_mercadoria
trechos_fisicos.linha → dim_linhas.nome_linha
```

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Python 3.8+** | Linguagem base |
| **Streamlit** | Framework web interativo |
| **Pandas** | Manipulação de dados |
| **SQLite** | Banco de dados relacional |
| **Plotly** | Visualizações interativas |
| **Git** | Controle de versão |


## 📖 Fonte de Dados

Os dados utilizados são provenientes da **Declaração de Rede 2025** publicada pela ANTT (Agência Nacional de Transportes Terrestres):

🔗 [Portal ANTT - Declaração de Rede](https://www.gov.br/antt/pt-br/assuntos/ferrovias/declaracao-de-rede)

### Conjuntos de Dados Utilizados:
1. **Pátios Ferroviários** - Características operacionais e tempos
2. **Terminais de Carga** - Capacidades por tipo de mercadoria
3. **Trechos Físicos** - Especificações técnicas da via
4. **Linhas Ferroviárias** - Informações dos corredores
5. **Mercadorias** - Classificação de cargas

## 🤝 Contribuições

Este é um projeto de portfólio pessoal desenvolvido como desafio técnico. Sugestões e feedback são bem-vindos!

[⬆️ Voltar ao topo](#-dashboard-antt---declaração-de-rede-ferroviária)

---
---
---

# 🇺🇸 English Version

# 🚆 ANTT Dashboard - Railway Network Declaration

Access the dashboard
[Deployed application ](https://antt-data-analysis.streamlit.app/)


> **Technical Challenge**: Data Engineering and Interactive Visualization with Python

A dashboard for analyzing Brazilian railway infrastructure, developed as part of a technical challenge that evaluates skills in ETL, data modeling, and interactive panel development.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**[🇧🇷 Ler em Português](#-dashboard-antt---declaração-de-rede-ferroviária)**

---

## 📋 About the Challenge

This project was developed in response to a technical challenge that simulates a real data engineering scenario. The goal is to demonstrate competencies in:

- **Data Ingestion**: Extraction from multiple sources (CSV, Excel)
- **Relational Modeling**: SQLite database structuring with relationships
- **ETL Pipeline**: Complete extraction, transformation, and loading process
- **Data Visualization**: Interactive dashboard with actionable insights
- **Software Architecture**: Modular, scalable, and well-documented code

### 🎯 Technical Requirements Met

✅ Ingestion of **3+ datasets** from Network Declaration (ANTT)  
✅ Relational modeling with coherent **keys and relationships**  
✅ Dashboard with **3+ interactive sections** and sidebar navigation  
✅ Interactive charts using **Plotly**  
✅ Structured and **documented** code  
✅ Git repository with **complete README**  
✅ Executable application with `streamlit run app.py`  

### 📊 Available Analyses

#### 1️⃣ Yard Licensing
- Impact of operational status on licensing times
- Identification of congested corridors
- Distribution analysis by railway line

#### 2️⃣ Terminal Capacity
- Capacity distribution by commodity type
- Automatic classification by sector (Mining, Agriculture, Construction)
- Ranking of largest terminals
- Treemap and pie chart visualization

#### 3️⃣ Load vs. Speed Relationship
- Physical trade-off between weight and authorized speed (VMA)
- Commercial speed analysis (VMC)
- Data consistency audit (VMC > VMA)
- Operational efficiency ranking by corridor

## 🏗️ Project Architecture

```
antt-railway-dashboard/
│
├── app.py                          # Dashboard entry point
├── run_etl.py                      # ETL pipeline entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore
│
├── config/                         # Centralized configuration
│   ├── settings.py                # Dashboard config
│   ├── translations.py            # i18n system (PT/EN)
│   └── etl_config.py              # ETL pipeline config
│
├── etl/                            # ETL Pipeline
│   ├── __init__.py
│   ├── extract.py                 # Raw data extraction
│   ├── transform.py               # Cleaning and transformation
│   ├── load.py                    # Loading into SQLite
│   ├── validators.py              # Quality validations
│   └── utils.py                   # Helper functions
│
├── src/                            # Dashboard Modules
│   ├── database/
│   │   └── queries.py             # Organized SQL queries
│   ├── data/
│   │   └── loader.py              # Loading with cache
│   ├── utils/
│   │   └── helpers.py             # Helper functions
│   └── pages/
│       ├── page_yards.py          # Page: Yards
│       ├── page_capacity.py       # Page: Capacity
│       └── page_speed.py          # Page: Speed
│
├── data/                           # Raw data (not versioned)
│   ├── raw/                       # Original CSV/Excel from ANTT
│   └── processed/                 # Processed data
│
└── db/
    └── data/
        └── antt.db                # SQLite database (generated by ETL)
```

## 🚀 How to Run

### Prerequisites
- Python 3.11
- Java JDK (for PySpark)
- pip (Python package manager)

### 1. Virtual Environment (Windows)

```powershell
# 1.1 Create venv
python -m venv venv

# 1.2 Activate environment
.\venv\Scripts\activate

# 1.3 Configure JAVA_HOME 
# Note: Check the path of your own Java instalation
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
```


### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run ETL Pipeline
```bash
python ./db/etl.py
```
> This command will:
> - Extract data from CSV/Excel files
> - Clean and transform the data
> - Create SQLite database in `db/data/antt.db`

### 4. Run Dashboard
```bash
streamlit run app.py
```

### 5. Access in Browser
```
http://localhost:8501
```

## 📊 Data Model

### Main Tables

**Fact Tables:**
- `patios` - Railway yards (licensing time, location)
- `terminais` - Cargo terminals (capacity by commodity)
- `trechos_fisicos` - Track segments (max load, speeds)

**Dimension Tables:**
- `dim_linhas` - Railway lines/corridors
- `dim_mercadorias` - Types of transported commodities

### Relationships
```
patios.id_linha → dim_linhas.id_linha
terminais.id_mercadoria → dim_mercadorias.id_mercadoria
trechos_fisicos.linha → dim_linhas.nome_linha
```

## 🛠️ Technology Stack

| Technology | Usage |
|------------|-------|
| **Python 3.8+** | Base language |
| **Streamlit** | Interactive web framework |
| **Pandas** | Data manipulation |
| **SQLite** | Relational database |
| **Plotly** | Interactive visualizations |
| **Git** | Version control |


## 📖 Data Source

The data used is from the **2025 Network Declaration** published by ANTT (National Land Transportation Agency):

🔗 [ANTT Portal - Network Declaration](https://www.gov.br/antt/pt-br/assuntos/ferrovias/declaracao-de-rede)

### Datasets Used:
1. **Railway Yards** - Operational characteristics and times
2. **Cargo Terminals** - Capacities by commodity type
3. **Physical Segments** - Technical track specifications
4. **Railway Lines** - Corridor information
5. **Commodities** - Cargo classification

## 🤝 Contributions

This is a personal portfolio project developed as a technical challenge. Suggestions and feedback are welcome!

[⬆️ Back to top](#-english-version)
