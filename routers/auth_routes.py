from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from dependencies import pegar_sessao, verificar_token
from database.models import Usuario
from schemas import UsuarioSchema, LoginSchema
from core.security import bcrypt_context


auth_router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


def criar_token(
    id_usuario: int,
    duracao_token: timedelta = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ),
):
    """
    Cria um JWT para o usuário informado.

    O token contém:
    - sub: ID do usuário
    - exp: data de expiração do token
    """

    data_expiracao = datetime.now(timezone.utc) + duracao_token

    payload = {
        "sub": str(id_usuario),
        "exp": data_expiracao,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def autenticar_usuario(
    email: str,
    senha: str,
    session: AsyncSession,
):
    """
    Busca um usuário pelo e-mail e verifica sua senha.

    Retorna o usuário caso as credenciais sejam válidas.
    Caso contrário, retorna None.
    """

    resultado = await session.execute(
        select(Usuario).where(Usuario.email == email)
    )

    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        return None

    if not bcrypt_context.verify(senha, usuario.senha):
        return None

    return usuario


@auth_router.get(
    "/",
    summary="Verificar rota de autenticação",
    description="""
    Retorna informações básicas sobre o módulo de autenticação.

    Esta rota não exige autenticação e pode ser utilizada
    para verificar se o endpoint de autenticação está disponível.
    """,
    response_description="Informações sobre o módulo de autenticação.",
)
async def home():
    return {
        "mensagem": "Você acessou a rota padrão de autenticação",
        "autenticado": False,
    }


@auth_router.post(
    "/criar_conta",
    summary="Criar uma nova conta",
    description="""
    Cria uma nova conta de usuário.

    O e-mail informado deve ser único no sistema.
    A senha recebida é criptografada antes de ser armazenada
    no banco de dados.

    Após o cadastro, o usuário é persistido no banco de dados.
    """,
    response_description="Confirmação de criação da conta.",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "O e-mail informado já está cadastrado."
        }
    },
)
async def criar_conta(
    usuario_schema: UsuarioSchema,
    session: AsyncSession = Depends(pegar_sessao),
):
    resultado = await session.execute(
        select(Usuario).where(
            Usuario.email == usuario_schema.email
        )
    )

    usuario = resultado.scalar_one_or_none()

    if usuario:
        raise HTTPException(
            status_code=400,
            detail="E-mail do usuário já cadastrado",
        )

    senha_criptografada = bcrypt_context.hash(
        usuario_schema.senha
    )

    novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=senha_criptografada,
        ativo=usuario_schema.ativo,
        admin=usuario_schema.admin,
    )

    session.add(novo_usuario)

    await session.commit()
    await session.refresh(novo_usuario)

    return {
        "mensagem": (
            f"Usuário cadastrado com sucesso: "
            f"{usuario_schema.email}"
        )
    }


@auth_router.post(
    "/login",
    summary="Realizar login",
    description="""
    Autentica um usuário utilizando e-mail e senha.

    Caso as credenciais sejam válidas, a API retorna:

    - access_token: utilizado para acessar recursos protegidos.
    - refresh_token: utilizado para obter um novo access token.
    - token_type: tipo do token, definido como bearer.

    O access token possui duração definida pela configuração
    ACCESS_TOKEN_EXPIRE_MINUTES.

    O refresh token possui duração de 7 dias.
    """,
    response_description="Tokens de autenticação.",
    responses={
        400: {
            "description": "Credenciais inválidas ou usuário não encontrado."
        }
    },
)
async def login(
    login_schema: LoginSchema,
    session: AsyncSession = Depends(pegar_sessao),
):
    usuario = await autenticar_usuario(
        login_schema.email,
        login_schema.senha,
        session,
    )

    if usuario is None:
        raise HTTPException(
            status_code=400,
            detail="Usuário não encontrado ou credenciais inválidas",
        )

    access_token = criar_token(usuario.id)

    refresh_token = criar_token(
        usuario.id,
        timedelta(days=7),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post(
    "/login-form",
    summary="Realizar login utilizando formulário OAuth2",
    description="""
    Realiza a autenticação utilizando o formato de formulário
    padrão do OAuth2.

    O campo username deve receber o e-mail do usuário e
    o campo password deve receber sua senha.

    Esta rota é especialmente útil para integração com o
    fluxo OAuth2 utilizado pela documentação do Swagger.
    """,
    response_description="Access token para autenticação.",
    responses={
        400: {
            "description": "Credenciais inválidas ou usuário não encontrado."
        }
    },
)
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(pegar_sessao),
):
    usuario = await autenticar_usuario(
        dados_formulario.username,
        dados_formulario.password,
        session,
    )

    if usuario is None:
        raise HTTPException(
            status_code=400,
            detail="Usuário não encontrado ou credenciais inválidas",
        )

    access_token = criar_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@auth_router.get(
    "/refresh",
    summary="Renovar access token",
    description="""
    Gera um novo access token utilizando o usuário autenticado.

    É necessário enviar um token válido para acessar esta rota.

    O usuário é identificado através do token fornecido pela
    dependência verificar_token.
    """,
    response_description="Novo access token.",
    responses={
        401: {
            "description": "Token inválido, expirado ou ausente."
        }
    },
)
async def use_refresh_token(
    usuario: Usuario = Depends(verificar_token),
):
    access_token = criar_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }