from flask import Flask, jsonify, request

app = Flask(__name__)
items = {}
next_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/items")
def list_items():
    return jsonify(list(items.values()))


@app.post("/items")
def create_item():
    global next_id
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return jsonify(error="'name' is required"), 400
    item = {"id": next_id, "name": name, "done": bool(data.get("done", False))}
    items[next_id] = item
    next_id += 1
    return jsonify(item), 201


@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify(error="not found"), 404
    return jsonify(item)


@app.put("/items/<int:item_id>")
def update_item(item_id):
    item = items.get(item_id)
    if item is None:
        return jsonify(error="not found"), 404
    data = request.get_json(silent=True) or {}
    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify(error="'name' must be a non-empty string"), 400
        item["name"] = data["name"]
    if "done" in data:
        item["done"] = bool(data["done"])
    return jsonify(item)


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    if items.pop(item_id, None) is None:
        return jsonify(error="not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)