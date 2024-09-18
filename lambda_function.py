import urllib.parse
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
        elif path == '/logged':
            return handle_logged(event)
        elif path == '/register':
            return handle_register(event)
        else:
            return {'statusCode': 404, 'body': 'Not Found'}
    elif http_method == 'POST':
        if path == '/cadastro/login':
            return handle_postlogin(event)
        elif path == '/register':
            return handle_registration(event)
        else:
            return {'statusCode': 404, 'body': 'Not Found'}
    
    return {'statusCode': 405, 'body': event}


def handle_login(event):
    with open('login.html', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()    
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'},'body': conteudo}

def handle_postlogin(event):
    try:
        parsed_data = urllib.parse.parse_qs(event.get('body'))
        username = parsed_data.get('username', [''])[0]
        password = parsed_data.get('password', [''])[0]

        if username == 'anonimo':
            username = 'anonimo@anonimo.com.br'
            senha = 'D9@0NAzn17W)'

        client = boto3.client('cognito-idp')

        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        print(response)

        resposta_logged = {nome: username, token: response['AuthenticationResult']['AccessToken']}

        return {'statusCode': 301, 'headers': {'Location': 'logged'}, 'body': json.dumps(resposta_logged)}
    except:
        return {'statusCode': 301, 'headers': {'Location': 'login'}}

def handle_logged(event):
    # Lógica para retornar a página de retorno do token
    dados = json.loads(event.get('body'))
    with open('logged.html', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

    conteudo = conteudo.replace('{{ Fulano }}', dados.nome)
    conteudo = conteudo.replace('{{ Token }}',dados.token)
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'}, 'body': conteudo}

def handle_register(event):
    # Lógica para retornar a página de registro
    with open('register.html', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'},'body': conteudo}

def handle_registration(event):
    # Lógica para processar registro de usuário
    return {'statusCode': 201, 'body': event}