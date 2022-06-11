import sqlalchemy
from pprint import pprint


def album_year():
    """название и год выхода альбомов, вышедших в 2018 году"""
    set = connection.execute(
        f"""
            SELECT title,release_year
            FROM album
            WHERE DATE_PART('year',release_year) = 2018;
        """
        ).fetchall()
    return set


def max_track():
    """название и продолжительность самого длительного трека"""
    set = connection.execute(
        f"""
            SELECT max(length)
            FROM track
        """
    ).fetchall()
    return set


def track_time():
    """название треков, продолжительность которых не менее 3,5 минуты"""
    set = connection.execute(
        f"""
            SELECT name
            FROM track
            WHERE length >= '00:03:30';
         """
    ).fetchall()
    return set


def collection():
    """названия сборников, вышедших в период с 2018 по 2020 год включительно"""
    set = connection.execute(
        f"""
                SELECT title
                FROM collection
                WHERE DATE_PART('year',release_year) Between 2018 and 2020;
        """
    ).fetchall()
    return set


def one_name_singer():
    """исполнители, чье имя состоит из 1 слова"""
    set = connection.execute(
        f"""
                SELECT name
                FROM singer
                WHERE name not LIKE '%% %%';
        """
    ).fetchall()
    return set


def track_my():
    """название треков, которые содержат слово "мой"/"my"""
    set = connection.execute(
        f"""
            SELECT name
            FROM track
            WHERE name LIKE '%%мой%%' or name LIKE '%%my%%' ;
         """
    ).fetchall()
    return set

engine = sqlalchemy.create_engine('postgresql://netology:pass@localhost:5432/singer_new')
connection = engine.connect()

# pprint(album_year(2018))
# pprint(max_track())
# pprint(track_time())
# pprint(collection())
# pprint(one_name_singer())
# pprint(track_my())