"""Utility helpers."""
from __future__ import annotations

from typing import List


def normalize(values: List[float]) -> List[float]:
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return [0.5] * len(values)
    return [(v - min_v) / (max_v - min_v) for v in values]
