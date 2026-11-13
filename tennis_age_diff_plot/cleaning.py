import json
import re
import pandas as pd


def _parse_matches(js_text):
    marker = re.search(r"\bvar\s+morematchmx\s*=\s*", js_text)
    if marker is None:
        raise ValueError("Could not find morematchmx in career JS")
    try:
        rows, _ = json.JSONDecoder().raw_decode(js_text[marker.end():].lstrip())
    except json.JSONDecodeError as exc:
        raise ValueError("Could not parse career-match array") from exc
    if not isinstance(rows, list):
        raise ValueError("Expected a list of career matches")
    return rows


def _age_at(match_date, birth_date):
    return (match_date - pd.Timestamp(birth_date)).days / 365.2425


def _opponent_age(value, match_date):
    value = str(value or "").strip()
    if re.fullmatch(r"\d{8}", value):
        dob = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        return _age_at(match_date, dob) if pd.notna(dob) else float("nan")
    return pd.to_numeric(value, errors="coerce")


def _clean_row(row, birth_date):
    if not isinstance(row, list) or len(row) < 17 or row[4] not in ("W", "L"):
        return None
    date = pd.to_datetime(row[0], format="%Y%m%d", errors="coerce")
    if pd.isna(date):
        return None
    player_age = _age_at(date, birth_date)
    opponent_age = _opponent_age(row[16], date)
    return {"date": date, "opponent": row[11], "result": row[4],
            "player_age": player_age, "opponent_age": opponent_age,
            "age_difference": player_age - opponent_age}


def _clean_matches(js_text, birth_date, player_name):
    rows = [_clean_row(row, birth_date) for row in _parse_matches(js_text)]
    data = pd.DataFrame(row for row in rows if row is not None)
    if data.empty:
        raise ValueError(f"No usable matches for {player_name}")
    data = data.dropna(subset=["player_age", "opponent_age"]).reset_index(drop=True)
    if data.empty:
        raise ValueError(f"No valid age pairs for {player_name}")
    data.attrs["player_name"] = player_name
    return data