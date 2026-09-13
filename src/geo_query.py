import urllib.request
import urllib.parse
import json
import ssl

# Base endpoint of the geocoding proxy service
SERVICE_URL = "http://py4e-data.dr-chuck.net/opengeo?"

# SSL context to avoid certificate verification issues (common in dev/learning setups)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def build_geocode_url(address: str) -> str:
    """
    Dynamically constructs a web-safe URL for the geocoding API
    by encoding the user's address input.

    Example:
        Input:  "Charminar, Hyderabad"
        Output: "http://py4e-data.dr-chuck.net/opengeo?q=Charminar%2C+Hyderabad"
    """
    params = {"q": address}
    encoded_params = urllib.parse.urlencode(params)
    full_url = SERVICE_URL + encoded_params
    return full_url

def fetch_geocode_data(url: str) -> str:
    """
    Sends a GET request to the geocoding API and retrieves the raw JSON response.

    Uses the global SSL context (ctx) to avoid certificate verification issues.
    """
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print(f"Retrieved {len(data)} characters")
    return data


if __name__ == "__main__":
    test_address = input("Enter location: ").strip()
    url = build_geocode_url(test_address)
    print(f"\nRetrieving: {url}")

    raw_data = fetch_geocode_data(url)
    print(raw_data[:300])


