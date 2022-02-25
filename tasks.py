from flask import jsonify

from utils import get_result


def get_actors(actor_1, actor_2):
    """Поиск всех кастов с двумя актерами"""
    sql = f'''SELECT netflix.cast 
    FROM netflix 
    WHERE netflix.cast LIKE '%{actor_1}%' AND netflix.cast LIKE '%{actor_2}%' '''

    result = get_result(sql)
    return result


def get_suite_actors(actor_1, actor_2):
    """Кто играет с actor_1 и actor_2 в паре больше 2 раз"""
    result = get_actors(actor_1, actor_2)

    # словарь "имя актера": "количество совпадений"
    all_actors = {}
    for actors_ in result:
        actors = actors_['cast']
        actors_list = actors.split(', ')

        for actor in actors_list:
            if actor != actor_1 and actor != actor_2:
                if actor not in all_actors.keys():
                    all_actors[actor] = 1
                else:
                    all_actors[actor] += 1

    suite_actors = []
    for actor in all_actors.keys():
        if all_actors[actor] > 2:
            suite_actors.append(actor)

    return suite_actors


def search_by_type_year_genre_page(type, year, genre):
    """Поиск по типу, дате выхода и жанру """

    genre = genre.title()

    if type.lower() == 'movie':
        type = f"'{type.title()}'"
    if type.lower() == 'tvshow':
        type = f"'TV Show'"

    sql = f'''SELECT title, description, listed_in
    FROM netflix 
    WHERE type = {type} AND release_year = {year} AND listed_in LIKE '%{genre}%' 
    LIMIT 10
                '''

    result = get_result(sql)

    return jsonify(result)


if __name__ == "__main__":
    actor_1 = 'Rose McIver'
    actor_2 = 'Ben Lamb'
    print(', '.join(get_suite_actors(actor_1, actor_2)))

    actor_1 = 'Jack Black'
    actor_2 = 'Dustin Hoffman'
    print(', '.join(get_suite_actors(actor_1, actor_2)))
