import sqlite3

rating = {
    "children": 'G',
    "family": "('G', 'PG', 'PG-13')",
    "adult": "('R', 'NC-17')"
}


def get_result(sql):
    """Получить ответ на запрос из базы"""

    result = []
    with sqlite3.connect('netflix.db') as con:
        con.row_factory = sqlite3.Row
        sqlite_query = sql
        for item in con.execute(sqlite_query).fetchall():
            result.append(dict(item))  # Выполняем запрос с помощью курсора

    return result


def get_film_by_title(sql):
    """Форматирование ответа для найденного по имени фильма"""

    result = get_result(sql)[0]
    movie_info = {
        "title": result["title"],
        "country": result["country"],
        "release_year": result["release_year"],
        "genre": result["listed_in"],
        "description": result["description"]
    }
    return movie_info
