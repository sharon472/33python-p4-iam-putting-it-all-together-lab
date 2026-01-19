from flask import Flask, request, jsonify, session
from models import db, User, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------- SIGNUP ----------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    image_url = data.get("image_url", "")
    bio = data.get("bio", "")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 422

    user = User(username=username, image_url=image_url, bio=bio)
    user.password = password
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify(user.to_dict()), 201


# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 422

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    session['user_id'] = user.id
    return jsonify(user.to_dict()), 200


# ---------- LOGOUT ----------
@app.route("/logout", methods=["DELETE"])
def logout():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    session.pop('user_id')
    return '', 204


# ---------- CHECK SESSION ----------
@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(user.to_dict()), 200


# ---------- RECIPES ----------
@app.route("/recipes", methods=["GET", "POST"])
def recipes_index():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "GET":
        return jsonify([r.to_dict() for r in user.recipes]), 200

    data = request.get_json() or {}
    title = data.get("title")
    instructions = data.get("instructions")
    minutes = data.get("minutes_to_complete")

    if not title or not instructions or not minutes:
        return jsonify({"error": "Invalid data"}), 422

    recipe = Recipe(title=title, instructions=instructions, minutes_to_complete=minutes, user=user)
    db.session.add(recipe)
    db.session.commit()
    return jsonify(recipe.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)
