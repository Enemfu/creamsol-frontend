# =============================================================================
# creamsol_main_api.py — CreamSol API  (FastAPI · Stateless · Privacy-first)
# =============================================================================
from dotenv import load_dotenv
load_dotenv()

import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from routers.cream_router_iniciante import router as router_iniciante
from routers.cream_router_intermediario import router as router_intermediario  # ativar depois
from routers.cream_router_profissional import router as router_profissional

# ── Logging seguro ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("creamsol")

# ── Rate limiting ─────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CreamSol API",
    description=(
        "API pública de análise patrimonial para carteiras Solana. "
        "Nenhum dado de utilizador é armazenado ou registado."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # TODO produção: ["https://creamsol.io"]
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Middleware de privacidade ──────────────────────────────────────────────────
@app.middleware("http")
async def middleware_sem_logs_de_dados(request: Request, call_next):
    response = await call_next(request)
    logger.debug("HTTP %s → %s", request.method, response.status_code)
    return response

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(router_iniciante, prefix="/v1", tags=["Iniciante"])
app.include_router(router_intermediario, prefix="/v1", tags=["Intermediário"])
app.include_router(router_profissional, prefix="/v1", tags=["Profissional"])

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok", "servico": "CreamSol API"}

# ── Arranque local ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("creamsol_main_api:app", host="0.0.0.0", port=8000, reload=False)