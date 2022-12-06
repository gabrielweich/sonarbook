from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.exception_handlers import add_exception_handlers
from src.api.routers import include_routers
from src.config.settings import settings

app = FastAPI(title="Sonarbook")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
add_exception_handlers(app)
include_routers(api_router)
app.include_router(api_router, prefix="/api")
