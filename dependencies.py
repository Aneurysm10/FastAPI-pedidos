from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from models import Usuario
from models import SessionLocal  # async_sessionmaker
from config import SECRET_KEY, ALGORITHM
from oauth2 import oauth2_schema


async def pegar_sessao():
    async with SessionLocal() as session:
        yield session


async def verificar_token(
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Acesso negado, verifique a validade do token"
        )

    resultado = await session.execute(
        select(Usuario).where(Usuario.id == id_usuario)
    )

    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Acesso inválido"
        )

    return usuario