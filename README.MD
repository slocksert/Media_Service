# Media Service

## Descrição
Este serviço recebe uma URL por meio de uma fila do RabbitMQ e, de acordo com a plataforma, seleciona o serviço adequado para processar esses dados, retornando-os por outra fila.

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/slocksert/Media_Service.git
    ```
2. Navegue até o diretório do projeto

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso
1. Certifique-se de que o WebDriver está no seu PATH
2. Execute o script principal:
    ```bash
    python main.py
    ```