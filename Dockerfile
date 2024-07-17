# Use uma imagem base do Python
FROM python:3.10.11

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação usará
EXPOSE 8000

# Define o comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]