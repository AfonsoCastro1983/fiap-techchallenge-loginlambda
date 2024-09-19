import urllib.parse
import base64
import boto3
import json
from botocore.exceptions import ClientError

USER_POOL_ID = 'us-east-2_ZrPiVhqeJ'
CLIENT_ID = '4jai8du53pd4hk8r0vigksoimf'

def lambda_handler(event, context):
    print('evento')
    print(event)
    # Extrai o caminho do endpoint da requisição
    path = event['path']
    http_method = event['httpMethod']

    # Roteamento básico baseado no caminho
    if http_method == 'GET':
        if path == '/cadastro/login':
            return handle_login(event)
        elif path == '/cadastro/register':
            return handle_register(event)
        else:
            return {'statusCode': 404, 'body': 'Not Found'}
    elif http_method == 'POST':
        if path == '/cadastro/logged':
            return handle_logged(event)
        elif path == '/cadastro/register':
            return handle_registration(event)
        else:
            return {'statusCode': 404, 'body': 'Not Found'}
    
    return {'statusCode': 405, 'body': event}

def load_html(name):
    with open(name, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

    with open("background-lanchonete.jpeg", "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')

    conteudo = conteudo.replace('{{ BACKGROUND }}', 'data:image/png;base64,'+base64_string)
    
    return conteudo

def handle_login(event):
    conteudo = load_html('login.html')
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'},'body': conteudo}

def handle_logged(event):
    # Lógica para retornar a página de retorno do token
    conteudo = load_html('logged.html')

    try:
        auth_pass = json.loads(event.get('body'))
        username = auth_pass['username']
        senha = auth_pass['password']

        parsed_data = urllib.parse.parse_qs(event.get('body'))
        username = parsed_data.get('username', [''])[0]
        senha = parsed_data.get('password', [''])[0]

        if username == 'anonimo':
            username = 'anonimo@anonimo.com.br'
            senha = '0jvFuo/n#06R'

        client = boto3.client('cognito-idp')

        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': senha
            }
        )

        resposta_logged = {nome: username, token: response['AuthenticationResult']['AccessToken']}

        conteudo = conteudo.replace('{{ Fulano }}', username)
        conteudo = conteudo.replace('{{ Token }}',resposta_logged)

        return {'statusCode': 200, 'headers': {'Content-type': 'text/html'}, 'body': conteudo}
    except:
        conteudo = conteudo.replace('{{ Fulano }}', 'Não Identificado')
        conteudo = conteudo.replace('{{ Token }}','')
        return {'statusCode': 200, 'headers': {'Content-type': 'text/html'}, 'body': conteudo}

def handle_register(event):
    # Lógica para retornar a página de registro
    conteudo = load_html('register.html')
    
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'},'body': conteudo}

def handle_registration(event):
    # Lógica para processar registro de usuário
    return {'statusCode': 201, 'body': event}