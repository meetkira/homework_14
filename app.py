import json

from flask import Flask
from utils import rating, get_result, get_film_by_title

app = Flask(__name__)


# http://127.0.0.1:5000/movie/9
@app.route("/movie/<string:title>")
def search_by_title_page(title):
    """Поиск фильма по названию"""

    sql = f'''SELECT title, country, release_year, listed_in, description 
    FROM netflix 
    WHERE title LIKE '%{title}%' AND type = 'Movie' 
    ORDER BY release_year DESC LIMIT 1
                '''

    result = get_film_by_title(sql)

    return app.response_class(response=json.dumps(result), status=200, mimetype="application/json")


# http://127.0.0.1:5000/movie/2020/to/2021
@app.route("/movie/<start>/to/<end>")
def search_by_range_page(start, end):
    """Поиск фильма по дате выхода в диапазоне"""

    if not start or not end:
        return "введите диапазон"

    sql = f'''SELECT title, release_year  
    FROM netflix 
    WHERE release_year BETWEEN {start} AND {end} AND type = 'Movie' 
    ORDER BY release_year LIMIT 100
                '''

    result = get_result(sql)

    return app.response_class(response=json.dumps(result), status=200, mimetype="application/json")


# http://127.0.0.1:5000/rating/family
@app.route("/rating/<string:rate>")
def search_by_rating_page(rate):
    """Поиск по рейтингу"""

    rate = rate.lower()
    if rate not in rating.keys():
        return "введите существующий рейтинг"

    if len(rating[rate]) > 1:
        suit_rate_sql = f"WHERE rating IN {rating[rate]}"
    else:
        suit_rate_sql = f"WHERE rating = '{rating[rate]}'"

    sql = f'''SELECT title, rating, description 
    FROM netflix 
    {suit_rate_sql} 
    LIMIT 100
                '''

    result = get_result(sql)

    return app.response_class(response=json.dumps(result), status=200, mimetype="application/json")


# http://127.0.0.1:5000/genre/comedies
@app.route("/genre/<string:genre>")
def search_by_genre_page(genre):
    """Поиск по жанру"""

    genre = genre.title()
    sql = f'''SELECT title, description 
        FROM netflix 
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC LIMIT 10
                    '''

    result = get_result(sql)

    return app.response_class(response=json.dumps(result), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run()
