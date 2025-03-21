import json

import redis


class Cacher(redis.Redis):
    tao_dividends_cache_key_format = "{netuid};{hotkey}"

    def get_json(self, name: bytes | str | memoryview) -> dict | list:
        s = self.get(name)
        return json.loads(s) if s else {}

    def set_json(self, name: bytes | str | memoryview, obj: dict | list):
        self.set(name, json.dumps(obj))

    def tao_dividends_cache_key(self, netuid: int | None, hotkey: str | None) -> str:
        return self.tao_dividends_cache_key_format.format(netuid=netuid, hotkey=hotkey)

    def get_tao_dividends(self, netuid: int | None, hotkey: str | None) -> dict | None:
        cache_key = self.tao_dividends_cache_key_format.format(
            netuid=netuid, hotkey=hotkey
        )
        return self.get_json(cache_key)

    def set_tao_dividends(
        self, netuid: int | None, hotkey: str | None, dividends: dict
    ) -> int | None:
        cache_key = self.tao_dividends_cache_key_format.format(
            netuid=netuid, hotkey=hotkey
        )
        return self.set_json(cache_key, dividends)


cache = Cacher(host="localhost", port=6379, decode_responses=True)
