from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String, default="")
    bio = db.Column(db.String, default="")

    recipes = db.relationship("Recipe", backref="user", cascade="all, delete-orphan")

    # password property
    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self._password_hash, plaintext)

    # Some tests expect authenticate()
    def authenticate(self, plaintext):
        return self.check_password(plaintext)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "image_url": self.image_url,
            "bio": self.bio,
            "recipes": [r.to_dict() for r in self.recipes]
        }


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructions": self.instructions,
            "minutes_to_complete": self.minutes_to_complete,
            "user_id": self.user_id
        }
