import asyncio

from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class StakeAction(Base):
    __tablename__ = "stake_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    hotkey: Mapped[str]
    rao: Mapped[int]


engine = create_async_engine("sqlite+aiosqlite://", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def setup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(setup())
