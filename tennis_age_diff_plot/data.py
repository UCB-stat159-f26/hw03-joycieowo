import re
import requests
import pandas as pd
from .cleaning import _clean_matches

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.tennisabstract.com/"
}
WIKIDATA_API = "https://www.wikidata.org/w/api.php"


def _normalize_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Player name must be a nonempty string")
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name.strip())
    return " ".join(name.split()).title()


def _player_slug(name):
    return re.sub(r"[^A-Za-z0-9]", "", _normalize_name(name))


def _fetch_matches(slug):
    url = f"https://www.tennisabstract.com/jsmatches/{slug}Career.js"
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        if response.status_code == 404:
            raise ValueError(f"No Tennis Abstract career data for '{slug}'. Check the name.")
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"Could not download Tennis Abstract matches: {exc}") from exc
    return response.text


def _wikidata_id(name):
    params = {"action": "wbsearchentities", "search": name, "language": "en",
              "format": "json", "limit": 15}
    response = requests.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    for item in response.json().get("search", []):
        if item.get("label", "").casefold() == name.casefold() and "tennis" in item.get("description", "").lower():
            return item["id"]
    raise ValueError(f"Could not identify tennis player '{name}' in Wikidata")


def _birth_date(name):
    identifier = _wikidata_id(name)
    params = {"action": "wbgetentities", "ids": identifier,
              "props": "claims", "format": "json"}
    response = requests.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    try:
        value = response.json()["entities"][identifier]["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
        return pd.Timestamp(value.lstrip("+")[:10])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ValueError(f"Birth date unavailable for '{name}'") from exc


def get_player_matches(name):
    """Return a DataFrame of career matches and age differences."""
    display_name = _normalize_name(name)
    js_text = _fetch_matches(_player_slug(display_name))
    try:
        birth_date = _birth_date(display_name)
    except requests.RequestException as exc:
        raise ConnectionError(f"Birth-date lookup failed: {exc}") from exc
    return _clean_matches(js_text, birth_date, display_name)