import aiogram

from .welcome import router as welcome_router
from .parsers import router as parsers_router
from .checkers import router as checkers_router
from .debank_checker import router as debank_checker_router
from .info import router as info_router

routers: list[aiogram.Router] = [
    welcome_router,
    parsers_router,
    checkers_router,
    info_router,
    debank_checker_router,
]