from flask import Flask, request, jsonify, redirect, send_from_directory
import json, os

app = Flask(__name__, static_folder="static")

DATA_FILE = "urls.json"

# Initialize JSON file if not present
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_urls():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_urls(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/go/<short_code>")
def go(short_code):
    data = load_urls()
    target_url = data.get(short_code)
    if target_url:
        return redirect(target_url)
    return jsonify({"error": "Short code not found"}), 404

@app.route("/api/add_url", methods=["POST"])
def add_url():
    req = request.get_json()
    short_code = req.get("short_code")
    target_url = req.get("target_url")

    if not short_code or not target_url:
        return jsonify({"error": "Missing fields"}), 400

    data = load_urls()
    data[short_code] = target_url
    save_urls(data)
    return jsonify({"message": "URL updated successfully"}), 200

@app.route("/api/list_urls")
def list_urls():
    return jsonify(load_urls())

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(port=5000)
