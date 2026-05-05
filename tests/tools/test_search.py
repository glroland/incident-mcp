import pytest
from datetime import date
from src.tools.search import search


def test_search_raises_when_no_params():
    with pytest.raises(ValueError, match="At least one search parameter must be specified"):
        search()


def test_search_by_hostname():
    pytest.skip("not implemented")


def test_search_by_start_date():
    pytest.skip("not implemented")


def test_search_by_end_date():
    pytest.skip("not implemented")


def test_search_by_date_range():
    pytest.skip("not implemented")


def test_search_by_hostname_and_date_range():
    pytest.skip("not implemented")


def test_search_returns_empty_when_no_matches():
    pytest.skip("not implemented")
