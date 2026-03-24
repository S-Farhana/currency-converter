"""
Currency Converter - CI/CD Demo App
Converts amounts between currencies using live exchange rates.
"""

import requests


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Fetch the exchange rate from an external API.
    Returns the rate as a float.
    Raises ValueError if currency codes are invalid.
    Raises ConnectionError if the API is unreachable.
    """
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if len(from_currency) != 3 or len(to_currency) != 3:
        raise ValueError(f"Invalid currency code. Use 3-letter codes like USD, INR, EUR.")

    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not connect to exchange rate API. Check your internet.")
    except requests.exceptions.HTTPError:
        raise ValueError(f"Currency '{from_currency}' not found or API error.")

    data = response.json()

    if to_currency not in data["rates"]:
        raise ValueError(f"Currency '{to_currency}' is not supported.")

    return data["rates"][to_currency]


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert an amount from one currency to another.
    Returns a dict with result details.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    # Same currency — no conversion needed
    if from_currency == to_currency:
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": 1.0,
            "result": round(amount, 2),
        }

    rate = get_exchange_rate(from_currency, to_currency)
    result = round(amount * rate, 2)

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "rate": round(rate, 6),
        "result": result,
    }


def main():
    """Interactive CLI for the currency converter."""
    print("=" * 40)
    print("   Currency Converter - CI/CD Demo")
    print("=" * 40)

    try:
        amount = float(input("\nEnter amount: "))
        from_cur = input("From currency (e.g. USD): ")
        to_cur   = input("To currency   (e.g. INR): ")

        data = convert_currency(amount, from_cur, to_cur)

        print("\n--- Result ---")
        print(f"  {data['amount']} {data['from']} = {data['result']} {data['to']}")
        print(f"  Exchange rate: 1 {data['from']} = {data['rate']} {data['to']}")
        print("-" * 40)

    except ValueError as e:
        print(f"\n[Error] {e}")
    except ConnectionError as e:
        print(f"\n[Network Error] {e}")


if __name__ == "__main__":
    main()