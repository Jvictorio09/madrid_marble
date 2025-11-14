import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict


CONTENT_PATH = Path(__file__).with_name("homepage.json")


@lru_cache
def get_homepage_content() -> Dict[str, Any]:
    try:
        with CONTENT_PATH.open(encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


