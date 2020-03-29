"""Environment operation helper module.
"""
import os
from typing import Any, Dict


EnvMap = Dict[str, str]
"""Environment variables"""


def filter_envmap(prefix: str, src: EnvMap = None, lowering: bool = True) -> EnvMap:
    """Filter source dict by that has prefix.
    IF ``lowering`` is ``True``, filtered dict' key is lower string.

    :param prefix: Filtering key-prefix
    :param src: Filtering target source dict
    :param lowering: Key lowering
    """
    if src is None:
        src = os.environ
    dst = {}
    plen = len(prefix)
    for k, v in src.items():
        if not k.startswith(prefix):
            continue
        k_ = k[plen:]
        if lowering:
            k_ = k_.lower()
        dst[k_] = v
    return dst


def parse_as_dict(
    value: str,
    pair_delimiter: str = None,
    kv_delimiter: str = None,
    convert: callable = None,
) -> Dict[str, Any]:
    pair_delimiter = "," if pair_delimiter is None else pair_delimiter
    kv_delimiter = ":" if kv_delimiter is None else kv_delimiter
    convert = str if convert is None else convert
    parsed = {}
    for pair in value.split(pair_delimiter):
        k, v = pair.split(kv_delimiter)
        parsed[k] = convert(v)
    return parsed
