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
   git clone [https://github.com/Aneurysm10/FastAPI-pedidos.git](https://github.com/Aneurysm10/FastAPI-pedidos.git)
   cd FastAPI-pedidos
