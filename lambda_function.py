import urllib.parse
import base64
import boto3
import json
import time
import requests
from botocore.exceptions import ClientError

USER_POOL_ID = 'us-east-2_Uvk12Ahpe'
CLIENT_ID = '1o0vfq0udn75k92psplrko7oji'

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

        response_user = client.get_user(
            AccessToken=response['AuthenticationResult']['AccessToken']
        )

        nome_usuario = next((item['Value'] for item in response_user['UserAttributes'] if item['Name'] == 'name'), None)

        conteudo = conteudo.replace('{{ Fulano }}', nome_usuario)
        conteudo = conteudo.replace('{{ Token }}',response['AuthenticationResult']['AccessToken'])

        return {'statusCode': 200, 'headers': {'Content-type': 'text/html'}, 'body': conteudo}
    except:
        conteudo = conteudo.replace('{{ Fulano }}', 'Não Identificado')
        conteudo = conteudo.replace('{{ Token }}','Verifique usuário e senha e tente novamente')
        return {'statusCode': 200, 'headers': {'Content-type': 'text/html'}, 'body': conteudo}

def handle_register(event):
    # Lógica para retornar a página de registro
    conteudo = load_html('register.html')    
    return {'statusCode': 200, 'headers': {'Content-type': 'text/html'},'body': conteudo}

def handle_registration(event):
    # Lógica para processar registro de usuário
    payload = json.loads(event.get('body'))
    client = boto3.client('cognito-idp')
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=payload.get('cpf'),
            Password=payload.get('password'),
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': payload.get('email')
                },
                {
                    'Name': 'name',
                    'Value': payload.get('nome')
                }
            ]
        )

        print('Response Cognito')
        print(response)

        time.sleep(2)

        resp_confirm = client.admin_confirm_sign_up(
            UserPoolId=USER_POOL_ID,
            Username=payload.get('cpf')
        )

        print('Confirmação Cognito')
        print(resp_confirm)

        #Cadastrar na aplicação da lanchonete
        payload = {
            "nome": payload.get('nome'),
            "idcognito": response.get('UserSub'),
            "email": payload.get('email'),
            "cpf": payload.get('cpf')
        }

        resp_lanchonete = requests.post("http://a6614520a11704e48a4c16e3d10c749c-851906114.us-east-2.elb.amazonaws.com/cliente", json=payload, headers={'Content-Type': 'application/json'})

        print('Criação usuário lanchonete')
        print(resp_lanchonete)

        return {'statusCode': 201, 'headers': {'Content-type': 'application/json'},'body': '{"cadastro": true}'}
    except client.exceptions.UsernameExistsException:
        return {'statusCode': 500, 'headers': {'Content-type': 'application/json'},'body': '{"cadastro": true, "error": "Usuário já existe"}'}
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Content-type': 'application/json'},'body': '{"cadastro": true, "error": '+str(e)+'}'}