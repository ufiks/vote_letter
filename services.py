from typing import List, Dict

from instances import redis


def initialize() -> None:
    init_keys = ['A', 'B', 'C', 'D']

    for key in init_keys:
        redis.set(key, 0)


def get_all_keys() -> List[str]:
    all_keys = list(redis.scan_iter("*"))

    return [key.decode() for key in all_keys]


def get_db() -> Dict[str, int]:
    db = {}

    for key in get_all_keys():
        value = redis.get(key)
        db[key] = value.decode()

    return db
