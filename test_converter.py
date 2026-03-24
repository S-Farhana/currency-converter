"""
Tests for Currency Converter - runs with pytest OR python3 directly
"""
import sys
from unittest.mock import patch, MagicMock
import requests as req
from converter import convert_currency, get_exchange_rate

def make_mock_response(rates):
    mock = MagicMock()
    mock.json.return_value = {"rates": rates}
    mock.raise_for_status.return_value = None
    return mock

# ── Tests for get_exchange_rate() ────────

def test_valid_conversion_returns_float():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"INR": 83.5})
        rate = get_exchange_rate("USD", "INR")
        assert rate == 83.5, f"Expected 83.5, got {rate}"

def test_invalid_currency_raises():
    try:
        get_exchange_rate("US", "INR")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid currency code" in str(e)

def test_unsupported_currency_raises():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"EUR": 0.92})
        try:
            get_exchange_rate("USD", "XYZ")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not supported" in str(e)

def test_network_error_raises():
    with patch("converter.requests.get", side_effect=req.exceptions.ConnectionError):
        try:
            get_exchange_rate("USD", "INR")
            assert False, "Should have raised ConnectionError"
        except ConnectionError as e:
            assert "Could not connect" in str(e)

# ── Tests for convert_currency() ─────────

def test_usd_to_inr():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"INR": 83.5})
        result = convert_currency(100, "USD", "INR")
        assert result["result"] == 8350.0
        assert result["from"] == "USD"
        assert result["to"] == "INR"
        assert result["rate"] == 83.5

def test_eur_to_usd():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"USD": 1.08})
        result = convert_currency(50, "EUR", "USD")
        assert result["result"] == 54.0

def test_zero_amount():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"EUR": 0.92})
        result = convert_currency(0, "USD", "EUR")
        assert result["result"] == 0.0

def test_same_currency_no_api_call():
    result = convert_currency(100, "USD", "USD")
    assert result["result"] == 100.0
    assert result["rate"] == 1.0

def test_negative_amount_raises():
    try:
        convert_currency(-50, "USD", "INR")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e)

def test_lowercase_codes_normalised():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"INR": 83.5})
        result = convert_currency(10, "usd", "inr")
        assert result["from"] == "USD"
        assert result["to"] == "INR"

def test_large_amount():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"INR": 83.5})
        result = convert_currency(1_000_000, "USD", "INR")
        assert result["result"] == 83_500_000.0

def test_result_dict_has_all_keys():
    with patch("converter.requests.get") as mock_get:
        mock_get.return_value = make_mock_response({"EUR": 0.92})
        result = convert_currency(100, "USD", "EUR")
        assert all(k in result for k in ["amount", "from", "to", "rate", "result"])

# ── Runner (for python3 test_converter.py) ──────────

if __name__ == "__main__":
    tests = [
        test_valid_conversion_returns_float,
        test_invalid_currency_raises,
        test_unsupported_currency_raises,
        test_network_error_raises,
        test_usd_to_inr,
        test_eur_to_usd,
        test_zero_amount,
        test_same_currency_no_api_call,
        test_negative_amount_raises,
        test_lowercase_codes_normalised,
        test_large_amount,
        test_result_dict_has_all_keys,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASSED  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAILED  {t.__name__}  →  {e}")
            failed += 1
    print(f"\n{passed + failed} tests: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)