# Fila de Atendimento OS
<h5>Versão 0.0.1

## Requisitos

- Python 3.x
- Token de bot do Telegram

## Configuração

1. Clone este repositório.
2. Crie um ambiente virtual usando `python -m venv venv`.
3. Instale as dependências usando `pip install -r requirements.txt`.
4. Configure o token do bot no arquivo `./conf/.env`.

## Uso

- Para começar, abra um chat com o bot e use `/start`.
- No primeiro acesso, será solicitado que você se registre.  
![Registro](https://i.ibb.co/Gnk5H4N/start.png)  
Após o registro, o bot coletará informações como nome e telefone para personalizar sua experiência de atendimento.
- Ao clicar em registrar, será solicitado que você forneça duas informações.  
![Nome](https://i.ibb.co/wWB9hRn/name.png)  
![Telefone](https://i.ibb.co/C9x7jXF/phone.png)
- Depois de se registrar, o menu para `Técnico Externo` será liberado. Por padrão, ele está configurado para entrar em contato com o NOC de uma empresa de redes. No entanto, é facilmente configurável. Basta editar o arquivo `./func/command.py` e procurar por "NOC" para fazer a substituição.  
![Menu](https://i.ibb.co/6yNYySN/menu.png)
- Para trocar do acesso de `Técnico Externo` para `Atendente`, basta editar manualmente o setor de `tecnico` para `noc` no arquivo JSON que foi criado no diretório `./sessions/`.

## Execução

Após a configuração, execute o bot utilizando o seguinte comando:

`python main.py`