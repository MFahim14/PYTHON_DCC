from flask import Flask, request, jsonify
import time
import sqlite3
import logging

app = Flask(__name__)

# Database setup
DATABASE = "inventory.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                name TEXT PRIMARY KEY,
                quantity INTEGER
            )
        """)
        conn.commit()

# Delay function
def delay():
    time.sleep(10)

# Endpoints
@app.route("/transform", methods=["POST"])
def transform():
    data = request.json
    print(f"Received transform data: {data}")
    delay()
    return jsonify({"message": "Transform data received"}), 200

@app.route("/translation", methods=["POST"])
def translation():
    data = request.json
    print(f"Received translation data: {data}")
    delay()
    return jsonify({"message": "Translation data received"}), 200

@app.route("/rotation", methods=["POST"])
def rotation():
    data = request.json
    print(f"Received rotation data: {data}")
    delay()
    return jsonify({"message": "Rotation data received"}), 200

@app.route("/scale", methods=["POST"])
def scale():
    data = request.json
    print(f"Received scale data: {data}")
    delay()
    return jsonify({"message": "Scale data received"}), 200

@app.route("/file-path", methods=["GET"])
def file_path():
    project_path = request.args.get("projectpath", "false").lower() == "true"
    path = "/path/to/project" if project_path else "/path/to/file"
    delay()
    return jsonify({"path": path}), 200

@app.route("/add-item", methods=["POST"])
def add_item():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")

    if not name or not quantity:
        return jsonify({"error": "Missing name or quantity"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()

    delay()
    return jsonify({"message": "Item added/updated"}), 200

@app.route("/remove-item", methods=["POST"])
def remove_item():
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE name = ?", (name,))
        conn.commit()

    delay()
    return jsonify({"message": "Item removed"}), 200

@app.route("/update-quantity", methods=["POST"])
def update_quantity():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")

    if not name or not quantity:
        return jsonify({"error": "Missing name or quantity"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (quantity, name))
        conn.commit()

    delay()
    return jsonify({"message": "Quantity updated"}), 200

# Initialize database
init_db()

if __name__ == "__main__":
    app.run(debug=True)