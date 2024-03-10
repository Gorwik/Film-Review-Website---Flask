from flask import Blueprint, request, flash, jsonify
from .models_handlers import NoteHandler, ForumCommentHandler
from . import cache
from .views import film
import json

data = Blueprint("data", __name__)

@data.route("/note", methods=["POST","PATCH","DELETE"])
def note():
    data = json.loads(request.data)
    user_id = int(data["user_id"])
    film_id = int(data["film_id"])

    cache.delete_memoized(film, str(film_id))

    if request.method == "DELETE":
        NoteHandler.delete(user_id=user_id, film_id=film_id)
        flash('Note was deleted!', category='success')
        return jsonify({})
        
    if not (note_data := data["note_data"]):
        flash('Note is too short!', category='error')
        return jsonify({})
        
    if request.method == "POST":
        NoteHandler.create(user_id=user_id, film_id=film_id, note_data=note_data)
        flash('Note added!', category='success')
        
    elif request.method == "PATCH":
        NoteHandler.update(user_id=user_id, film_id=film_id, note_data=note_data)
        flash('Note updated!', category='success')
        
    return jsonify({})

@data.route("/forum-comment", methods=["POST","PATCH","DELETE"])
def forum_comment():
    data = json.loads(request.data)
    film_id = int(data["film_id"])
    cache.delete_memoized(film, str(film_id))
    
    if request.method == "DELETE":
        comment_id = data["comment_id"]
        ForumCommentHandler.delete(forum_comment_id=comment_id)
        flash('Comment was deleted!', category='success')
        return jsonify({})
    
    if not (comment_data := data["comment_data"]):
        flash('Comment is too short!', category='error')
        return jsonify({})
    
    user_id = int(data["user_id"])
    if request.method == "POST":
        ForumCommentHandler.create(user_id=user_id, film_id=film_id, forum_comment_data=comment_data)
        flash('Comment added!', category='success')
        return jsonify({})
        
    if request.method == "PATCH":
        parent_comment_id = int(data["parent_comment_id"])
        ForumCommentHandler.create(user_id=user_id, film_id=film_id, forum_comment_data=comment_data, parent_forum_comment_id = parent_comment_id)
        flash('Reply added!', category='success')
        return jsonify({})