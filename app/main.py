from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import auth_routes, post_routes
from app.db import Base, engine

app = FastAPI(title="MVC FastAPI App")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_routes.router)
app.include_router(post_routes.router)

@app.get("/")
def root():
    # return {"message": "FastAPI MVC App is running. Visit /docs to use the API."}
    RedirectResponse(url="/docs")
