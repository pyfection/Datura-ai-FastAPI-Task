import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends, Query, HTTPException, Security
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api import db
from api.stake_extrinsic_sentiment import get_twitter_sentiment
from api.tasks import update_stake_extrinsic
from api.utils import get_tao_dividends as get_tao_dividends_

REQUIRED_TOKEN = os.getenv("API_AUTH_TOKEN")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.setup()
    yield


app = FastAPI(lifespan=lifespan, debug=True)

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
    trade: bool = Query(False, description="Trade"),
    token: str = Depends(get_auth_token),
):
    """Protected endpoint that returns the Tao dividends data for a given subnet and hotkey."""
    dividends, is_cached = await get_tao_dividends_(netuid, hotkey)
    if trade:
        sentiment = get_twitter_sentiment(netuid)
        update_stake_extrinsic.delay(sentiment, netuid, hotkey)
    return {
        "netuid": netuid,
        "hotkey": hotkey,
        "dividends": dividends,
        "timestamp": datetime.now().isoformat(),
        "cached": is_cached,
        "stake_tx_triggered": trade,
    }


app.include_router(api_v1)
