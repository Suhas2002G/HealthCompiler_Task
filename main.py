from fastapi import FastAPI
from core.database import Base, engine
from router.contact_router import router as contact_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contact Book-API")

app.include_router(contact_router)