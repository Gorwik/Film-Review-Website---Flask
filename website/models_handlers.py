from .models import Note, ForumComment, User
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import contains_eager
from abc import ABC, abstractmethod
class BaseHandler(ABC):
    @abstractmethod
    def get():
        pass
    
    @abstractmethod
    def create():
        pass
    
    @abstractmethod
    def update():
        pass
    
    @abstractmethod
    def delete():
        pass

class NoteHandler(BaseHandler):
    
    @staticmethod
    def get(user_id, film_id):
        return Note.query.filter_by(user_id = user_id, film_id = film_id).first()
    
    @staticmethod
    def create(user_id, film_id, note_data):
        new_note = Note(data=note_data, user_id=user_id, film_id=film_id) #providing the schema for the note 
        db.session.add(new_note) #adding the note to the database 
        db.session.commit()
        
    @staticmethod
    def update(user_id, film_id, note_data):
        note = Note.query.filter_by(user_id = user_id, film_id = film_id).first()
        note.data = note_data
        note.date = func.now()
        db.session.commit()
        
    @staticmethod
    def delete(user_id, film_id):
        note = Note.query.filter_by(user_id = user_id, film_id = film_id).first()
        db.session.delete(note)
        db.session.commit()
        
class ForumCommentHandler(BaseHandler):
    
    @staticmethod
    def get(film_id):
        names = {}
        forum_comments: list[ForumComment] = []
        forum_comments_with_names = db.session.query(ForumComment, User.first_name)\
                        .filter(ForumComment.film_id == film_id)\
                        .join(User, ForumComment.user_id==User.id)\
                        .all()
        for forum_comment, name in forum_comments_with_names:
            names[forum_comment.user_id] = name
            forum_comments.append(forum_comment)
            
        return forum_comments, names
    
    @staticmethod
    def create(user_id, film_id, forum_comment_data, parent_forum_comment_id = None):
        new_forum_comment = ForumComment(data=forum_comment_data, user_id=user_id, film_id=film_id, parent_forum_comment_id = parent_forum_comment_id) #providing the schema for the note 
        db.session.add(new_forum_comment) #adding the note to the database 
        db.session.commit()
        
    @staticmethod
    def delete(forum_comment_id):
        forum_comment = ForumComment.query.filter_by(id = forum_comment_id).first()
        replies = forum_comment.replies.all()
        for reply in replies:
            db.session.delete(reply)
        db.session.delete(forum_comment)
        db.session.commit()