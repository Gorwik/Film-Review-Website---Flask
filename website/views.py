from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .films_db_API import API
from .models_handlers import NoteHandler, ForumCommentHandler
from . import cache

api = API()
GENRES = api.genres
YEARS = tuple(range(2024, 1900, -1))
RATING = tuple(range(0, 11))

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        cache.delete("films_list")
        title = request.form.get("title")
        genre = request.form.get("genre")
        year = request.form.get("year")
        rate = request.form.get("rate")
        if not (
            films_list := api.get_film_by_params(
                title=title, genre=genre, year=year, rate=rate
            )
        ):
            flash(
                "Loading the content is unavailble now, try to refresh the page or try to use it later.",
                category="error",
            )
        else:
            cache.set("films_list", films_list)
        return render_template(
            "home.html",
            films=films_list,
            user=current_user,
            years=YEARS,
            rating=RATING,
            genres=GENRES,
        )

    if not (films_list := cache.get("films_list")):
        if not (films_list := api.get_film_by_params()):
            flash(
                "Loading the content is unavailble now, try to refresh the page or try to use it later.",
                category="error",
            )
        else:
            cache.set("films_list", films_list)

    return render_template(
        "home.html",
        films=films_list,
        user=current_user,
        years=YEARS,
        rating=RATING,
        genres=GENRES,
    )


@views.route("/film/<id>")
@cache.memoize()
def film(id: int):
    id = int(id)

    if not (film := api.get_film_by_id(id=id)):
        flash(
            "Loading the content is unavailble now, try to refresh the page or try to use it later.",
            category="error",
        )
        return redirect(url_for("views.home"))

    forum_comments, names = ForumCommentHandler.get(id)

    if not current_user.is_authenticated:
        return render_template(
            "film.html",
            user=current_user,
            film=film,
            forum_comments=forum_comments,
            names=names,
        )

    if note := NoteHandler.get(user_id=current_user.id, film_id=id):
        note = note.data
    else:
        note = None

    return render_template(
        "film_authenticated.html",
        film=film,
        user=current_user,
        note=note,
        forum_comments=forum_comments,
        names=names,
    )
