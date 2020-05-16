from blog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default="default_profile.jpg")
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    hashed_password = db.Column(db.String(64))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"User {self.username}"


class Post(db.Model):

    users = db.relationship(User)

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(64))
    text = db.Column(db.Text)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.date = datetime.utcnow()
        self.user_id = user_id

    def __repr__(self):
        return f"[{self.date}] {self.title}\n\n{self.text}"