from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config.settings import settings

engine = create_async_engine(settings.SQL_ALCHEMY__DATABASE_URL, echo=False)

session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
