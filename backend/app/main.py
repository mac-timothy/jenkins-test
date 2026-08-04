from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from swagger_ui_bundle import swagger_ui_path

from app.database.database import engine, Base
from app.models import user
from app.routes import auth


# Create database tables
Base.metadata.create_all(
    bind=engine
)


# Create FastAPI application
app = FastAPI(
    title="Jenkins Test FastAPI Backend",
    description="Authentication API",
    version="1.0.0",
    docs_url=None
)


# --------------------------------------------------
# Force OpenAPI version to 3.0.3
# --------------------------------------------------

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Change OpenAPI version
    openapi_schema["openapi"] = "3.0.3"

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


# --------------------------------------------------
# Serve Swagger UI files locally
# --------------------------------------------------

app.mount(
    "/swagger-static",
    StaticFiles(directory=swagger_ui_path),
    name="swagger-static"
)


# --------------------------------------------------
# Custom Swagger documentation
# --------------------------------------------------

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():

    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/swagger-static/swagger-ui-bundle.js",
        swagger_css_url="/swagger-static/swagger-ui.css",
    )


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(
    auth.router
)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Welcome to the FastAPI application!"
    }