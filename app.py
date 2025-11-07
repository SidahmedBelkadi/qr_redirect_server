from flask import Flask, request, jsonify, redirect, send_from_directory
import json, os

app = Flask(__name__, static_folder="static")

DATA_FILE = "urls.json"

# Initialize JSON file with new structure
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
    """Redirect to the target URL"""
    data = load_urls()
    redirect_data = data.get(short_code)
    
    if not redirect_data:
        return jsonify({"error": "Short code not found"}), 404

    target_url = redirect_data.get("url")
    if not target_url:
        return jsonify({"error": "Invalid redirect data"}), 500

    return redirect(target_url)

@app.route("/api/add_url", methods=["POST"])
def add_url():
    """Create a new redirect"""
    req = request.get_json()
    short_code = req.get("short_code")
    user = req.get("user")
    url = req.get("url")

    if not short_code or not user or not url:
        return jsonify({"error": "Missing required fields"}), 400

    data = load_urls()
    
    # Check if short_code already exists
    if short_code in data:
        return jsonify({"error": "Short code already exists"}), 409

    data[short_code] = {
        "user": user,
        "url": url
    }
    
    save_urls(data)
    return jsonify({"message": "Redirect created successfully", "short_code": short_code}), 201

@app.route("/api/update_url/<short_code>", methods=["PUT"])
def update_url(short_code):
    """Update an existing redirect"""
    req = request.get_json()
    user = req.get("user")
    url = req.get("url")

    if not user or not url:
        return jsonify({"error": "Missing required fields"}), 400

    data = load_urls()
    
    if short_code not in data:
        return jsonify({"error": "Short code not found"}), 404

    data[short_code] = {
        "user": user,
        "url": url
    }
    
    save_urls(data)
    return jsonify({"message": "Redirect updated successfully"}), 200

@app.route("/api/delete_url/<short_code>", methods=["DELETE"])
def delete_url(short_code):
    """Delete a redirect"""
    data = load_urls()
    
    if short_code not in data:
        return jsonify({"error": "Short code not found"}), 404

    del data[short_code]
    save_urls(data)
    return jsonify({"message": "Redirect deleted successfully"}), 200

@app.route("/api/list_urls")
def list_urls():
    """List all redirects"""
    return jsonify(load_urls())

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)