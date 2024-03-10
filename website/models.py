from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    __tablename__ = "note"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    film_id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default = func.now()) #trzeba potem zmienic default na ustawienie w momnecie kreowania notatki
    
    def __repr__(self) -> str:
        return f"Self id: {self.id}\nUser id: {self.user_id}\nFilm id: {self.film_id}\n"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    note = db.relationship('Note', backref='user', lazy=True)
    forum_comment = db.relationship('ForumComment', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"User id: {self.id}\nEmail: {self.email}\n"

class ForumComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    film_id = db.Column(db.Integer)
    parent_forum_comment_id = db.Column(db.Integer, db.ForeignKey('forum_comment.id'), nullable=True)
    replies = db.relationship('ForumComment', backref=db.backref('parent_comment', remote_side=[id]), lazy='dynamic')
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    data = db.Column(db.String(10000))

    def __repr__(self):
        return f'Comment id: {self.id}, Film id: {self.film_id}, User id: {self.user_id}, Parent Comment id: {self.parent_forum_comment_id}'