# Use uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requirements primeiro
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código da aplicação
COPY . .

# Expõe a porta que o Streamlit usa por padrão
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "dashboards.py", "--server.port=8501", "--server.address=0.0.0.0"]