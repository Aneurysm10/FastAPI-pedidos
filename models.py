from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Engine assíncrono
DATABASE_URL = "sqlite+aiosqlite:///database/banco.db"

db = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Session assíncrona
SessionLocal = async_sessionmaker(
    bind=db,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base
class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    senha: Mapped[str] = mapped_column(String)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String, default="PENDENTE")
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    preco: Mapped[float] = mapped_column(Float, default=0.0)
    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido", cascade="all, delete-orphan")

    def calcular_preco(self):
        # percorrer todos os itens do pedido
        # somar todos os preços de todos os itens dos pedidos
        # editar no campo "preço" o valor final do preço do pedido
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade: Mapped[int] = mapped_column(Integer)
    sabor: Mapped[str] = mapped_column(String)
    tamanho: Mapped[str] = mapped_column(String)
    preco_unitario: Mapped[float] = mapped_column(Float)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    pedido: Mapped["Pedido"] = relationship(back_populates="itens")