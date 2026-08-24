from flask import Flask, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Otani", "age": 24},
    {"id": 2, "name": "Tanaka", "age": 30}
]

# ユーザー一覧を取得
@app.route("/users", methods=["GET"])
def get_users():
    return users

# ユーザーを新規作成
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "age": data["age"]
    }

    users.append(new_user)

    return new_user, 201

# ユーザー情報を一部更新
@app.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    data = request.get_json()

    for user in users:
        if user["id"] == id:
            if "name" in data:
                user["name"] = data["name"]
            if "age" in data:
                user["age"] = data["age"]

            return user, 200

        return {"message": "User not found"}, 404

# ユーザーを消去
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    for user in users:
        if user["id"] == id:
            users.remove(user)

            return {"message": "User deleted"}, 200

    return {"message": "User not found"}, 404

app.run(debug=True, port=5000)