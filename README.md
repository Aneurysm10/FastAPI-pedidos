<div align="center">

# 🚀 API de Gerenciamento de Pedidos

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

Uma API RESTful assíncrona para gerenciamento de pedidos e usuários desenvolvida com **FastAPI**, **SQLAlchemy (Async)** e **SQLite**.

</div>

---

## 📌 Sobre o Projeto

Esta aplicação oferece uma estrutura robusta para controle de usuários, autenticação via tokens JWT e gerenciamento de pedidos com cálculo automático de preços e múltiplos itens por pedido.

### 🌟 Funcionalidades Principais
- **Autenticação Segura:** Cadastro e login de usuários com geração de token JWT.
- **Operações Assíncronas:** Utilização do `SQLAlchemy` assíncrono com driver `aiosqlite`.
- **Cálculo Automático:** Atualização dinâmica do valor total dos pedidos com base nos itens cadastrados.
- **Documentação Automática:** Swagger UI e ReDoc nativos e acessíveis no navegador.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM Assíncrono:** SQLAlchemy (AsyncSession)
- **Banco de Dados:** SQLite (`aiosqlite`)
- **Autenticação:** JWT (JSON Web Tokens) & Passlib / Bcrypt

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Git instalado na máquina.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Aneurysm10/FastAPI-pedidos.git
   cd FastAPI-pedidos
   ```
   2. **Crie um ambiente virtual:**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual:**

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

4. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite+aiosqlite:///database/banco.db
```

6. **Execute as migrations:**

```bash
alembic upgrade head
```

7. **Inicie o servidor:**

```bash
uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📚 Documentação da API

O FastAPI fornece documentação automática através do Swagger UI e ReDoc.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)** para autenticação dos endpoints protegidos.

O fluxo de autenticação funciona da seguinte forma:

```text
Cadastro
   ↓
Login
   ↓
Token JWT
   ↓
Authorization: Bearer <token>
   ↓
Endpoint protegido
```

Após realizar o login, o token deve ser enviado através do header:

```http
Authorization: Bearer SEU_TOKEN
```

---

## 👤 Usuários

O sistema possui funcionalidades para gerenciamento e autenticação de usuários.

Principais operações:

- Cadastro de usuários
- Login
- Geração de token JWT
- Validação de token
- Proteção de endpoints
- Hash de senhas

As senhas são armazenadas utilizando hash, evitando o armazenamento de credenciais em texto puro.

---

## 📦 Pedidos

Um pedido pode possuir múltiplos itens.

Exemplo:

```text
Pedido
│
├── Item 1
├── Item 2
└── Item 3
```

Cada item possui informações relacionadas ao produto, quantidade e preço.

O valor total do pedido é calculado automaticamente com base nos itens associados.

Exemplo:

```text
Produto A
Quantidade: 2
Preço: R$ 10,00

Produto B
Quantidade: 1
Preço: R$ 25,00

--------------------
Total: R$ 45,00
```

---

## 🗄️ Banco de Dados

O projeto utiliza **SQLite** como banco de dados e **SQLAlchemy** como ORM.

A comunicação com o banco é realizada de forma assíncrona utilizando:

- `AsyncSession`
- `aiosqlite`

As alterações na estrutura do banco são controladas através do **Alembic**.

---

## 🔄 Migrations

Para criar uma nova migration automaticamente:

```bash
alembic revision --autogenerate -m "descricao_da_mudanca"
```

Para aplicar as migrations:

```bash
alembic upgrade head
```

Para voltar uma migration:

```bash
alembic downgrade -1
```

---

## 📡 Principais Endpoints

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| `POST` | `/auth/login` | Realiza login | ❌ |
| `POST` | `/usuarios/` | Cria usuário | ❌ |
| `GET` | `/pedidos/` | Lista pedidos | 🔒 |
| `POST` | `/pedidos/` | Cria pedido | 🔒 |

---

## 🧪 Testando a API

Depois de iniciar o servidor, acesse o Swagger:

```text
http://127.0.0.1:8000/docs
```

Através dele é possível visualizar e testar os endpoints diretamente pelo navegador.

Também é possível utilizar ferramentas como:

- Postman
- Insomnia
- Bruno
- cURL

Exemplo:

```bash
curl http://127.0.0.1:8000/pedidos/
```

Para endpoints protegidos:

```bash
curl -H "Authorization: Bearer SEU_TOKEN" http://127.0.0.1:8000/pedidos/
```

---

## 🏗️ Estrutura do Projeto

```text
FastAPI-pedidos/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── database/
│   └── banco.db
│
├── routers/
│   ├── auth.py
│   └── pedidos.py
│
├── models.py
├── schemas.py
├── dependencies.py
├── config.py
├── main.py
├── alembic.ini
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🎯 Objetivos de Aprendizado

Este projeto foi desenvolvido para praticar conceitos importantes de desenvolvimento backend com Python:

- Desenvolvimento de APIs REST
- FastAPI
- Programação assíncrona
- SQLAlchemy 2.0
- AsyncSession
- Relacionamentos entre tabelas
- Pydantic
- Autenticação JWT
- Hash de senhas
- Dependency Injection
- Alembic e migrations
- Organização de projetos Python
- Documentação automática de APIs

---

## 📖 Aprendizados

Durante o desenvolvimento deste projeto, foram explorados conceitos fundamentais para a construção de aplicações backend modernas com Python.

O projeto permitiu colocar em prática a criação de uma API REST, comunicação assíncrona com banco de dados, autenticação utilizando JWT, validação de dados, relacionamento entre entidades e gerenciamento de migrations com Alembic.

---

## 👨‍💻 Autor

Desenvolvido por **Aneurysm10**.

### 🔗 Links

- GitHub: https://github.com/Aneurysm10
- Repositório: https://github.com/Aneurysm10/FastAPI-pedidos

---

<div align="center">

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório!

</div>
