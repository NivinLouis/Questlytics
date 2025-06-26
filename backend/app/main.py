from fastapi import FastAPI
from upload import router as upload_router
from database import Base, engine

print("✅ Running actual main.py")

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(upload_router)
