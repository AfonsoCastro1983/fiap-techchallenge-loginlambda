# Login Lambda - Fiap Tech Challenge

Esta função AWS Lambda implementa um sistema básico de autenticação e registro de usuários usando o Amazon Cognito. Ela serve páginas HTML para login e registro, manipulando as credenciais dos usuários e interagindo com o Cognito para confirmar e autenticar usuários.

## Funcionalidades

- **Login de Usuários**: Valida credenciais através do Cognito e retorna uma página com o token de acesso.
- **Registro de Usuários**: Realiza o registro de novos usuários no Cognito, solicitando email, nome e CPF.
- **Confirmação Automática**: Confirma automaticamente novos usuários após o registro, sem necessidade de verificação via e-mail.
- **Interfaces HTML**: Serve páginas web dinâmicas para login, registro e autenticação.

## Estrutura do Projeto

- `lambda_function.py`: Lógica principal da função Lambda.
- `login.html`, `register.html`, `logged.html`: Páginas HTML exibidas ao usuário.
- `background-lanchonete.jpeg`: Imagem de fundo embutida nas páginas HTML.
- `requirements.txt`: Dependências do projeto (boto3, etc.).

## Como logar no sistema de API's?

Este endpoint processa o login do usuário, seja através de credenciais fornecidas (usuário e senha) ou de forma anônima. Após o login bem-sucedido, um token é gerado e exibido ao usuário. Esse token deverá ser utilizado em todas as consultas subsequentes à API da Lanchonete FIAP, garantindo o acesso autenticado aos recursos da aplicação.

### Fluxo de Acesso:

1. O usuário acessa `/cadastro/login` e insere suas credenciais ou escolhe a opção de login anônimo.
2. Ao fazer login via `/cadastro/logged`, a função Lambda valida o usuário e retorna um token de acesso.
3. Esse token deve ser incluído nas próximas requisições para as APIs protegidas da Lanchonete FIAP.

## Requisitos

- AWS Lambda
- Amazon Cognito
- Dependências listadas em `requirements.txt`

## Como Usar

1. **Login**:
   - Endpoint: `/cadastro/login`
   - Retorna a página de login. Após o envio das credenciais, valida o usuário e exibe o token ou uma mensagem de erro.

2. **Registro**:
   - Endpoint: `/cadastro/register`
   - Permite o cadastro de novos usuários, solicitando email, nome, CPF e senha. Realiza o registro e confirma o usuário automaticamente.

3. **Login Anônimo/Usuário Logado**:
   - Endpoint: `/cadastro/logged`
   - Gera um token para usuários registrados ou anônimos. Esse token deverá ser utilizado para consultas futuras na API da Lanchonete FIAP.

### Link do API Gateway

Link atual: https://6c88dkaufi.execute-api.us-east-2.amazonaws.com/lanchonete/cadastro/login

## Instalação

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
