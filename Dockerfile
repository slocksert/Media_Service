# Use uma imagem base que tenha o Python (ou outra linguagem, conforme sua aplicação)
FROM python:3.10-slim

# Instala as dependências do sistema para o Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && apt-get clean

# Instala o Chrome e o ChromeDriver
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && CHROMEDRIVER_VERSION=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Copie os arquivos da aplicação para dentro do container
WORKDIR /app
COPY . .

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Comando para rodar a aplicação
CMD ["python", "main.py"]