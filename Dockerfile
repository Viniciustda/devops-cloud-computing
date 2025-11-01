# Imagem Base - imagem oficial do Python 3.11, versão slim
FROM python:3.11-slim-bullseye

# Diretório de Trabalho
WORKDIR /app

# Instala dependências
COPY requirements.txt .

# Instala as bibliotecas listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o Código da Aplicação
# Copia o script da API e o modelo
COPY app.py .

# Informa ao Docker que esta aplicação usa a porta 50031
EXPOSE 50031

# Comando de Execução
# O comando que será executado quando o container iniciar.
CMD ["flask", "run", "--host=0.0.0.0", "--port=50031"]