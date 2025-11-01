# Imagem Base
FROM python:3.11-slim-bullseye

# Diretório de Trabalho
WORKDIR /app

# Instala Dependências
COPY requirements.txt .

# Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o Código da Aplicação
# Copia o script de geração de regras
COPY generate_rules.py .

# Comando de Execução
# O comando para rodar quando o container iniciar.
# Ele apenas executa o script uma vez e depois termina.
CMD ["python", "generate_rules.py"]