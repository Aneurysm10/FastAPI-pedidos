from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import pegar_sessao, verificar_token
from models import ItemPedido, Pedido, Usuario
from schemas import ItemPedidoSchema, PedidoSchema, ResponsePedidoSchema

order_router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verificar_token)],
)


@order_router.get("/")
async def pedidos():
    """
    Rota inicial de verificação do módulo de pedidos.
    Confirma se o usuário autenticado possui acesso ao grupo de rotas.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}


@order_router.post("/pedido", status_code=status.HTTP_201_CREATED)
async def criar_pedido(
    pedido_schema: PedidoSchema,
    session: AsyncSession = Depends(pegar_sessao),
):
    """
    Cria um novo pedido para o usuário informado.
    Registra a instância inicial do pedido no banco de dados e retorna o ID gerado.
    """
    novo_pedido = Pedido(usuario_id=pedido_schema.usuario_id)

    session.add(novo_pedido)
    await session.commit()
    await session.refresh(novo_pedido)

    return {
        "mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"
    }


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Altera o status de um pedido existente para 'CANCELADO'.
    Permissão necessária: Usuário dono do pedido ou Administrador.
    """
    resultado = await session.execute(
        select(Pedido).where(Pedido.id == id_pedido)
    )
    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    # Apenas o administrador ou o dono do pedido pode cancelar
    if not (usuario.admin or usuario.id == pedido.usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa modificação",
        )

    pedido.status = "CANCELADO"

    await session.commit()
    await session.refresh(pedido)

    return {
        "mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
        "pedido": pedido,
    }


@order_router.get("/listar")
async def listar_pedidos(
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Retorna a lista completa de todos os pedidos cadastrados no sistema.
    Permissão necessária: Apenas Administradores.
    """
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa operação",
        )

    pedidos = (await session.scalars(select(Pedido))).all()
    return {"pedidos": pedidos}


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int,
    item_pedido_schema: ItemPedidoSchema,
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Adiciona um novo item (quantidade, sabor, tamanho, preço unitário) a um pedido existente
    e atualiza o valor total do pedido.
    Permissão necessária: Usuário dono do pedido ou Administrador.
    """
    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == id_pedido)
    )

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não existente",
        )

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa operação",
        )

    item_pedido = ItemPedido(
        quantidade=item_pedido_schema.quantidade,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        preco_unitario=item_pedido_schema.preco_unitario,
        pedido_id=id_pedido,
    )

    session.add(item_pedido)
    pedido.calcular_preco()

    await session.commit()

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco,
    }


@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Remove um item de um pedido pelo seu ID e recalcula o preço total do pedido restante.
    Permissão necessária: Usuário dono do pedido ou Administrador.
    """
    item_pedido = await session.scalar(
        select(ItemPedido).where(ItemPedido.id == id_item_pedido)
    )

    if not item_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no pedido não existente",
        )

    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == item_pedido.pedido_id)
    )

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa operação",
        )

    await session.delete(item_pedido)
    await session.flush()

    pedido.calcular_preco()

    await session.commit()
    await session.refresh(pedido)

    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido,
    }


@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(
    id_pedido: int,
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Conclui o fluxo do pedido alterando o seu status para 'FINALIZADO'.
    Permissão necessária: Usuário dono do pedido ou Administrador.
    """
    resultado = await session.execute(
        select(Pedido).where(Pedido.id == id_pedido)
    )
    pedido = resultado.scalar_one_or_none()

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    if not (usuario.admin or usuario.id == pedido.usuario_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa modificação",
        )

    pedido.status = "FINALIZADO"

    await session.commit()
    await session.refresh(pedido)

    return {
        "mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
        "pedido": pedido,
    }


@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(
    id_pedido: int,
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Exibe os detalhes de um pedido específico com a contagem dos seus itens.
    Permissão necessária: Usuário dono do pedido ou Administrador.
    """
    pedido = await session.scalar(
        select(Pedido).where(Pedido.id == id_pedido)
    )

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem autorização para fazer essa operação",
        )

    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido,
    }


@order_router.get(
    "/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema]
)
async def listar_pedidos_usuario(
    session: AsyncSession = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Retorna apenas os pedidos pertencentes ao usuário atualmente autenticado.
    Os dados retornados são filtrados através do 'ResponsePedidoSchema'.
    """
    pedidos = (
        await session.scalars(
            select(Pedido).where(Pedido.usuario_id == usuario.id)
        )
    ).all()

    return pedidos