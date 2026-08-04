from fastapi import FastAPI


from app.database.database import engine, Base

from app.models import user


from app.routes import auth



Base.metadata.create_all(
    bind=engine
)



app = FastAPI(

    title="Jenkins Test FastAPI Backend",

    description="Authentication API",

    version="1.0.0"

)



app.include_router(
    auth.router
)



@app.get("/")
def root():

    return {

        "message": "Welcome to the FastAPI application!"

    }