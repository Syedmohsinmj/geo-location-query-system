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
    """
    params = {"q": address}
    encoded_params = urllib.parse.urlencode(params)
    full_url = SERVICE_URL + encoded_params

    print("\n[build_geocode_url]")
    print(f"  Input  (typed): {address}")
    print(f"  Output (encoded URL): {full_url}")

    return full_url

def fetch_geocode_data(url: str) -> str:
    """
    Sends a GET request to the geocoding API and retrieves the raw JSON response.

    Uses the global SSL context (ctx) to avoid certificate verification issues.
    """
    print("\n[fetch_geocode_data]")
    print(f"  Input  (URL received): {url}")

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    print(f"  Output (raw JSON): {len(data)} characters")
    return data

def extract_location_data(raw_json: str) -> dict:
    """
    Parses the raw JSON string and extracts lat, lon, formatted address,
    and place_id from the first matching feature.

    Returns None if no results were found (empty 'features' list).
    """
    print("\n[extract_location_data]")
    print(f"  Input  (raw JSON): {len(raw_json)} characters")

    js = json.loads(raw_json)

    if not js.get("features"):
        print("  Output: no features found -> None")
        return None

    props = js["features"][0]["properties"]

    result = {
        "lat": props.get("lat"),
        "lon": props.get("lon"),
        "formatted_address": props.get("formatted"),
        "place_id": props.get("place_id"),
    }

    print(f"  Features found: {len(js['features'])} (using the first one)")
    print(f"  Output (extracted dict): {result}")
    return result

def display_result(location_data: dict):
    """
    Prints the extracted location data in a clean, formatted way.
    If location_data is None, prints a 'not found' message instead.
    """
    if location_data is None:
        print("\n[NO MATCH FOUND]")
        print("The address you entered could not be located.")
        return

    print("\n[MATCH FOUND]")
    print(f"Formatted Address: {location_data['formatted_address']}")
    print(f"Latitude: {location_data['lat']}")
    print(f"Longitude: {location_data['lon']}")
    print(f"Place ID: {location_data['place_id']}")


if __name__ == "__main__":
    print("--- GEO-LOCATION SERVICE ---")
    address = input("Enter location: ").strip()

    url = build_geocode_url(address)
    raw_data = fetch_geocode_data(url)
    location_data = extract_location_data(raw_data)
    display_result(location_data)

    print("\n--- TRANSACTION COMPLETE ---")


