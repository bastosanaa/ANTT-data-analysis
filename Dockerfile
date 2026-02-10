# 1. Imagem base oficial do Python (Slim é mais leve)
FROM python:3.11-slim

# 2. Variáveis de ambiente para evitar arquivos .pyc e logs de buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. INSTALAÇÃO DO JAVA (Crítico para o PySpark)
# O PySpark precisa da JVM para rodar as transformações
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean;

# 4. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 5. Copiar as dependências e instalar
# Copiamos apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo o resto do código do projeto para dentro do container
COPY . .

# 7. Expor a porta que o Streamlit usa
EXPOSE 8501

# 8. Comando para rodar a aplicação
# Ajuste o nome 'app.py' se o seu ficheiro principal tiver outro nome (ex: main.py)
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]