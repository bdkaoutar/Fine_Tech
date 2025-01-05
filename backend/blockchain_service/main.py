import uvicorn
from fastapi import FastAPI
from Fine_Tech.backend.blockchain_service.blockchain.routes import blockchain_router
from database.main import init_db

app = FastAPI()

# Inclure les routes blockchain
app.include_router(blockchain_router)

@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
