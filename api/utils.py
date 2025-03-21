import asyncio
import os

import bittensor as bt
from bittensor.core.chain_data import decode_account_id

from api.caching import cache


async def get_tao_dividends(
    netuid: int | None, hotkey: str | None
) -> (dict[int, dict[str, int]], bool):
    dividends = cache.get_tao_dividends(netuid, hotkey)
    is_cached = True
    if not dividends:
        is_cached = False
        dividends = await fetch_tao_dividends_per_subnet(netuid, hotkey)
        cache.set_tao_dividends(netuid, hotkey, dividends)
    return dividends, is_cached


async def fetch_tao_dividends_per_subnet(
    netuid: int | None, hotkey: str | None
) -> dict[int, dict[str, int]]:
    subtensor = bt.AsyncSubtensor()

    netuids = [netuid] if netuid else range(1, 51)
    result = {}
    for netuid in netuids:
        query_map_result = await subtensor.query_map(
            "SubtensorModule", "TaoDividendsPerSubnet", params=[netuid]
        )
        async for key, value in query_map_result:
            decoded_key = decode_account_id(key)
            if not hotkey or decoded_key == hotkey:
                result[netuid] = {decoded_key: value.value}

    return result


async def main():
    netuid = int(os.getenv("NETUID_DEFAULT"))
    hotkey = os.getenv("HOTKEY_DEFAULT")

    dividends = await fetch_tao_dividends_per_subnet(netuid, hotkey)

    if dividends is not None:
        print(f"Tao Dividends for hotkey {hotkey} on subnet {netuid}: {dividends}")
    else:
        print(f"No Tao dividends found for hotkey {hotkey} on subnet {netuid}")


if __name__ == "__main__":
    asyncio.run(main())
