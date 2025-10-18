# Use uma imagem base oficial do Python.
# python:3.9-slim-buster é uma boa escolha, pois é leve.
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /dashboards

# Copia o arquivo requirements.txt para o diretório de trabalho.
# Isso permite que o Docker utilize o cache de camadas se as dependências não mudarem.
COPY requirements.txt .

# Instala as dependências do Python.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código da sua aplicação para o diretório de trabalho.
COPY . .

# Expõe a porta que a aplicação Flask vai usar (padrão do Flask é 5000).
EXPOSE 5000

# Comando para rodar a aplicação quando o contêiner for iniciado.
CMD ["python", "app.py"]