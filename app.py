from flask import Flask, render_template, request, jsonify
from src.geo_query import build_geocode_url, fetch_geocode_data, extract_location_data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    address = request.args.get("q", "").strip()

    if not address:
        return jsonify({"found": False, "error": "Please enter a location."}), 400

    try:
        url = build_geocode_url(address)
        raw = fetch_geocode_data(url)
        data = extract_location_data(raw)
    except Exception:
        return jsonify({"found": False, "error": "Could not reach the geocoding service."}), 502

    trace = {
        "typed": address,
        "url": url,
        "json_chars": len(raw),
        "extracted": data,
    }

    if data is None:
        return jsonify({"found": False, "error": "No match found for that location.", "trace": trace})

    return jsonify({"found": True, "result": data, "trace": trace})


if __name__ == "__main__":
    app.run(debug=True)