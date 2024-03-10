import os
import requests
from pydantic import BaseModel


class Film(BaseModel):
    id: int
    title: str
    genre_ids: list[int]
    genre: str
    poster_path: str
    release_date: str
    overview: str
    vote_average: float
    popularity: float


class FilmExtended(Film):
    budget: int
    original_title: str
    production_countries: str
    production_companies: str


class API:
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    DEFAULT_IMAGE_URL = "https://cdn.ican.pl/minimized/v2/M1024xM2048xA/reader-files/book/BLp2nDil/1602758475/cover.jpg"
    IMAGE_PREFIX_URL = "https://image.tmdb.org/t/p/w500"

    def __init__(self) -> None:
        self.genres = self._get_genres()

    def get_film_by_params(self, title="", genre="", year="", rate=""):
        language = "en_US"
        page = 1

        if title:
            url = "https://api.themoviedb.org/3/search/movie"
            querystring = {
                "api_key": self.TMDB_API_KEY,
                "language": language,
                "page": page,
                "query": title,
            }
        else:
            url = "https://api.themoviedb.org/3/discover/movie"
            querystring = {
                "api_key": self.TMDB_API_KEY,
                "language": language,
                "page": page,
                "with_genres": genre,
                "primary_release_year": year,
                "vote_average.gte": rate,
            }

        response = requests.get(url, params=querystring)

        if not response.status_code == 200:
            return False

        film_models = self._create_film_models(response.json())
        return film_models

    def get_film_by_id(self, id: int):
        language = "en_US"
        url = f"https://api.themoviedb.org/3/movie/{id}"
        querystring = {
            "api_key": self.TMDB_API_KEY,
            "language": language,
        }
        response = requests.get(url, params=querystring)

        if not response.status_code == 200:
            return False

        film_extended_model = self._create_film_extended_model(response.json())
        return film_extended_model

    def _create_film_models(self, results):
        film_list: list[Film] = []
        for film_stats in results["results"]:
            film_id = film_stats["id"]
            title = film_stats["title"]
            genre_ids = film_stats["genre_ids"]
            if sufix_url := film_stats["poster_path"]:
                poster_path = self.IMAGE_PREFIX_URL + sufix_url
            else:
                poster_path = self.DEFAULT_IMAGE_URL
            release_date = film_stats.get("release_date", "Not found")
            overview = film_stats["overview"]
            vote_average = film_stats["vote_average"]
            popularity = film_stats["popularity"]
            genre = ", ".join([self.genres[genre_id] for genre_id in genre_ids])

            film_list.append(
                Film(
                    id=film_id,
                    title=title,
                    genre_ids=genre_ids,
                    genre=genre,
                    poster_path=poster_path,
                    release_date=release_date,
                    overview=overview,
                    vote_average=vote_average,
                    popularity=popularity,
                )
            )

        return film_list

    def _create_film_extended_model(self, film_stats):
        production_countries = []
        production_companies = []
        genre_ids = []
        genre = []

        film_id = film_stats["id"]
        title = film_stats["title"]
        original_title = film_stats["original_title"]
        if sufix_url := film_stats["poster_path"]:
            poster_path = self.IMAGE_PREFIX_URL + sufix_url
        else:
            poster_path = self.DEFAULT_IMAGE_URL
        release_date = film_stats.get("release_date", "Not found")
        overview = film_stats["overview"]
        vote_average = film_stats["vote_average"]
        popularity = film_stats["popularity"]
        budget = film_stats["budget"]
        for production_name, production_container in (
            ("production_countries", production_countries),
            ("production_companies", production_companies),
        ):
            for production in film_stats[production_name]:
                production_container.append(production["name"])
        production_countries = ", ".join(production_countries)
        production_companies = ", ".join(production_companies)
        for genre_ in film_stats["genres"]:
            genre_ids.append(genre_["id"])
            genre.append(genre_["name"])
        genre = ", ".join(genre)

        film = FilmExtended(
            id=film_id,
            title=title,
            original_title=original_title,
            genre_ids=genre_ids,
            genre=genre,
            poster_path=poster_path,
            release_date=release_date,
            overview=overview,
            vote_average=vote_average,
            popularity=popularity,
            budget=budget,
            production_countries=production_countries,
            production_companies=production_companies,
        )

        return film

    def _get_genres(self):
        url_genres = (
            f"https://api.themoviedb.org/3/genre/movie/list?api_key={self.TMDB_API_KEY}"
        )
        response = requests.get(url_genres)
        if not response.status_code == 200:
            print(response.text)
            return False
        else:
            genres = dict()
            for id_name_dict in response.json()["genres"]:
                id, name = id_name_dict.values()
                genres[id] = name
            return genres
