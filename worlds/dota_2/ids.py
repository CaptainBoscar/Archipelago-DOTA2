"""Ids of every location and item, frozen in data/ids.json so that game updates don't move them.

A name keeps its id forever, even once the game drops it; new names go at the end
(python -m worlds.dota_2.tools.update_ids).
"""
import json
import logging
from importlib import resources

with resources.files(__package__).joinpath("data/ids.json").open("r", encoding="utf-8") as _f:
    _IDS = json.load(_f)
LOCATION_IDS: dict[str, int] = _IDS["locations"]
ITEM_IDS: dict[str, int] = _IDS["items"]


_provisional: dict[int, dict[str, int]] = {}


def id_of(ids: dict[str, int], name: str) -> int:
    """The name's frozen id. A name not in data/ids.json yet gets a provisional one after the last, so that the world
    still loads and update_ids (which imports it) can register the name; FrozenIds fails until it does."""
    if name in ids:
        return ids[name]
    extra = _provisional.setdefault(id(ids), {})
    if name not in extra:
        logging.warning(f"{name!r} has no id in data/ids.json: run python -m worlds.dota_2.tools.update_ids")
        extra[name] = max(ids.values()) + 1 + len(extra)
    return extra[name]
