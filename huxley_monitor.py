#!/usr/bin/env python3
"""
Monitor Huxley Apartments for two-bedroom availability.
Exit code 0 = available, 1 = not available, 2 = error.
GitHub Actions uses the exit code to trigger notifications.
"""

import requests
import re
import sys
from datetime import datetime

URL = "https://www.equityapartments.com/san-francisco-bay/redwood-city/huxley-apartments"


def fetch_page() -> str:
    """Fetch the apartment listing page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def check_two_bedroom_availability(html: str) -> dict:
    """
    Check if two-bedroom apartments are available.
    Returns dict with availability status and details.
    """
    result = {
        "available": False,
        "details": [],
    }

    # Method 1: Check for pricing in 2-bed section
    # When available it shows pricing like "$X,XXX+"
    # When unavailable it shows "Coming soon"
    two_bed_pattern = r'2\s*Bed[^$]*?(\$[\d,]+\+?)'
    price_match = re.search(two_bed_pattern, html, re.IGNORECASE | re.DOTALL)

    if price_match:
        result["available"] = True
        result["details"].append(f"Price found: {price_match.group(1)}")

    # Method 2: Check JSON data embedded in page for AvailableUnits
    json_pattern = r'"UnitTypeDescription"\s*:\s*"2\s*Bed[^"]*"[^}]*"AvailableUnits"\s*:\s*\[([^\]]*)\]'
    json_match = re.search(json_pattern, html)

    if json_match and json_match.group(1).strip():
        result["available"] = True
        result["details"].append("Units found in JSON data")

    # Method 3: Look for specific unit listings with 2BR
    unit_pattern = r'2\s*(?:Bed|BR|Bedroom)[^<]*?(?:Available|Move-in|Ready)'
    if re.search(unit_pattern, html, re.IGNORECASE):
        result["available"] = True
        result["details"].append("Available units text found")

    # Check for "Coming soon" specifically for 2-bed (indicates NOT available)
    coming_soon_pattern = r'2\s*Bed[^<]*Coming\s*soon'
    if re.search(coming_soon_pattern, html, re.IGNORECASE | re.DOTALL):
        if not result["available"]:
            result["details"].append("Shows 'Coming soon'")

    return result


def main():
    print(f"Checking Huxley Apartments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {URL}")
    print("-" * 50)

    try:
        html = fetch_page()
        result = check_two_bedroom_availability(html)

        print(f"Two-bedroom available: {result['available']}")
        if result["details"]:
            print(f"Details: {', '.join(result['details'])}")

        if result["available"]:
            print("\n*** TWO-BEDROOM AVAILABLE! ***")
        else:
            print("\nNo two-bedroom units available yet")

        # Exit code: 0 = available, 1 = not available
        sys.exit(0 if result["available"] else 1)

    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
