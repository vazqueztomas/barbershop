from .haircuts import router as haircuts_router
from .auth import router as auth_router

__all__ = ["haircuts_router", "auth_router"]