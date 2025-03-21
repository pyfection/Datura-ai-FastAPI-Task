import os
from datetime import datetime

from fastapi import FastAPI, Depends, Query, HTTPException, Security
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.utils import fetch_tao_dividends_per_subnet

REQUIRED_TOKEN = os.getenv("API_AUTH_TOKEN")

app = FastAPI()

api_v1 = APIRouter(prefix="/api/v1", tags=["v1"])

security = HTTPBearer(
    auto_error=False
)  # auto_error to not make it raise 403 if no token is given


def get_auth_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dependency to handle authorization."""
    token = credentials.credentials if credentials else None

    if not token or token != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    return token


@api_v1.get("/tao_dividends")
async def get_tao_dividends(
    netuid: int = Query(None, description="Network UID"),
    hotkey: str = Query(None, description="Hotkey"),
    token: str = Depends(get_auth_token),
):
    """Protected endpoint that returns the Tao dividends data for a given subnet and hotkey."""
    dividends = await fetch_tao_dividends_per_subnet(netuid, hotkey)
    return {
        "netuid": netuid,
        "hotkey": hotkey,
        "dividends": dividends,
        "timestamp": datetime.now().isoformat(),
    }


app.include_router(api_v1)
