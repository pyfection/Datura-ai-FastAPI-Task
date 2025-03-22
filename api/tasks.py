import os

import redis
import bittensor as bt
from bittensor import Balance
from bittensor_wallet import Wallet

from api.celery_config import app

BITTENSOR_WALLET_NETWORK = os.environ.get("BITTENSOR_WALLET_NETWORK")
BITTENSOR_WALLET_NAME = os.environ.get("BITTENSOR_WALLET_NAME", "default")
BITTENSOR_WALLET_HOTKEY_NAME = os.environ.get("BITTENSOR_WALLET_HOTKEY_NAME", "default")
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.task(name="tasks.delete_redis_key")
def delete_redis_key(key):
    redis_client.delete(key)


@app.task(name="tasks.update_stake_extrinsic")
async def update_stake_extrinsic(sentiment: int, netuid: int, hotkey: str):
    subtensor = bt.Subtensor(network=BITTENSOR_WALLET_NETWORK)
    wallet = Wallet(
        name=BITTENSOR_WALLET_NAME,
        hotkey=BITTENSOR_WALLET_HOTKEY_NAME,
    )

    # print("BALANCE:", await subtensor.get_balance(wallet.coldkeypub.ss58_address))
    stake = Balance.from_tao(0.01 * sentiment, netuid)
    if sentiment > 0:
        subtensor.add_stake(wallet, hotkey_ss58=hotkey, netuid=netuid, amount=stake)
    else:
        subtensor.unstake(wallet, hotkey_ss58=hotkey, netuid=netuid, amount=stake)
