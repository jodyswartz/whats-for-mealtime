import os
import random
from typing import List


def load_food_list(file_path: str) -> List[str]:
    """
    Loads food list from a text file. Supports:
    - one item per line
    - or space-separated items on a single line (fallback)
    """
    if not file_path:
        return []

    if not os.path.exists(file_path):
        # don't crash if missing
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        if not raw:
            return []

        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        if len(lines) >= 2:
            return lines

        # fallback: single line space-separated
        return [x.strip() for x in raw.split() if x.strip()]
    except Exception:
        return []


def pick_random_food(foods: List[str]) -> str:
    if not foods:
        return ""
    return random.choice(foods)