import asyncio
import uvicorn
from app.app import app
from app.utils.init_roles import init_roles


if __name__ == "__main__":
    asyncio.run(init_roles())
    uvicorn.run(app, host="0.0.0.0", port=8000)
