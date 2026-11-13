from pathlib import Path

import pandas as pd
import pytest

from tennis_age_diff_plot.cleaning import _parse_matches, _clean_matches
from tennis_age_diff_plot.data import _player_slug, get_player_matches
from tennis_age_diff_plot.plotting import plot_player_ages

FIXTURES = Path(__file__).parent / "mockup_JS_content"


def _read_fixture(filename):
    return (FIXTURES / filename).read_text(encoding="utf-8")


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("Tests must not access the internet")
    monkeypatch.setattr("requests.get", refuse)


def test_player_names():
    assert _player_slug("serena williams") == "SerenaWilliams"
    assert _player_slug("Serena Williams") == "SerenaWilliams"
    assert _player_slug("SerenaWilliams") == "SerenaWilliams"


def test_female_matches():
    js_text = _read_fixture("FemalePlayerCareer.js")
    data = _clean_matches(js_text, "1981-09-26", "Serena Williams")
    assert len(data) == 3
    assert data.loc[0, "opponent_age"] == pytest.approx(18.78, abs=0.02)
    assert data.loc[0, "result"] == "L"


def test_male_matches():
    js_text = _read_fixture("MalePlayerCareer.js")
    data = _clean_matches(js_text, "1986-06-03", "Rafael Nadal")
    assert len(data) == 3
    assert data.loc[0, "opponent_age"] == pytest.approx(22.264202601)
    assert data.loc[2, "age_difference"] < 0


def test_invalid_js():
    with pytest.raises(ValueError, match="morematchmx"):
        _parse_matches("Invalid JS content")


def test_public_function(monkeypatch):
    js_text = _read_fixture("FemalePlayerCareer.js")
    monkeypatch.setattr("tennis_age_diff_plot.data._fetch_matches", lambda slug: js_text)
    monkeypatch.setattr("tennis_age_diff_plot.data._birth_date", lambda name: pd.Timestamp("1981-09-26"))
    data = get_player_matches("SerenaWilliams")
    assert len(data) == 3
    assert data.attrs["player_name"] == "Serena Williams"


def test_invalid_player(monkeypatch):
    def invalid(slug):
        raise ValueError(f"Player '{slug}' was not found")
    monkeypatch.setattr("tennis_age_diff_plot.data._fetch_matches", invalid)
    with pytest.raises(ValueError, match="not found"):
        get_player_matches("GastonSanchez")


def test_plot():
    js_text = _read_fixture("MalePlayerCareer.js")
    data = _clean_matches(js_text, "1986-06-03", "Rafael Nadal")
    ax = plot_player_ages(data)
    assert len(ax.collections) == 2
    assert "Rafael Nadal" in ax.get_title()
    ax.figure.clf()