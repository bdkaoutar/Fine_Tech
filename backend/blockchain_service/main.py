from fastapi import FastAPI
from blockchain.routes import blockchain_routes

# Création de l'application FastAPI
app = FastAPI()

# Enregistrement des routes
app.include_router(blockchain_routes, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
print("Routes enregistrées :", app.routes)
