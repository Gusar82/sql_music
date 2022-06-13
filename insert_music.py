import requests, sqlalchemy
from pprint import pprint


def get_topradio(dict_collections: dict, limit=0):
    """ Возращает словрь топ радио(плейлист) Deezer в кол-ве limit (0 = all)
        где: ключ - id радио
             значение - названия радио
    """
    url = "https://api.deezer.com/radio/top/"
    querystring = {'limit': limit}
    response = requests.request("GET", url, params=querystring)
    for collect in response.json()['data']:
        #print(collect['id'], collect['title'])
        dict_collections[collect['id']] = collect['title']
    return


def get_tracks_from_radio(id, limit=0):
    """
    Возращает список треков(json)
    """
    url = f"https://api.deezer.com/radio/{str(id)}/tracks/"
    querystring = {'limit': limit}
    response = requests.request("GET", url, params=querystring)
    return response.json()['data']


def getgenre_from_album(id_album):
    """
    Возращает жанр альбома
    """
    url = f"https://api.deezer.com/album/{str(id_album)}/"
    response = requests.request("GET", url)
    return response.json()['genres']['data'][0]


def get_from_album(id_album):
    """
    Возращает дату выхода альбома и жанр альбома
    """
    url = f"https://api.deezer.com/album/{str(id_album)}/"
    response = requests.request("GET", url).json()
    try:
        res_data = response['release_date']
        res_genre = response['genres']['data'][0]
    except (KeyError, IndexError):
        return None, None, None
    return res_data, res_genre['id'], res_genre['name']


def Insert_from_top_radio(dict_collections, limit=0):
    """
    Добавляет в БД Collection(Сборник) из плейлиста radio
    """
    get_topradio(dict_collections, limit)
    for key, value in dict_collections.items():
        connection.execute(
            f"""
                   INSERT INTO Collection(id,title,release_year)
                   VALUES ({key},'{value}',NOW())
                   ON CONFLICT (id) DO UPDATE 
                         SET title = excluded.title,
                             release_year = excluded.release_year;
                   """
        )
    return


def Insert_from_radio(id_radio, limit=0):
    for track in get_tracks_from_radio(id_radio, limit=limit):

        album_id = track['album']['id']
        title_album = track['album']['title'].replace("'", "")
        release_year = get_from_album(album_id)[0]
        if release_year == None:
            print(f"альбом {album_id} отсутствует")
            continue

        singer_id = track['artist']['id']
        singer_name = track['artist']['name'].replace("'", "")

        track_id = track['id']
        track_title = track['title'].replace("'", "")
        track_length = track['duration']

        style_id = get_from_album(album_id)[1]
        style_name = get_from_album(album_id)[2]

        connection.execute(
            f"""
                       INSERT INTO album(id,title,release_year)
                       VALUES ({album_id},'{title_album}','{release_year}')
                       ON CONFLICT (id) DO UPDATE 
                            SET title = excluded.title;
                       
                       INSERT INTO singer(id,name)
                       VALUES ({singer_id},'{singer_name}')
                       ON CONFLICT (id) DO UPDATE 
                            SET name = excluded.name;
                       
                       INSERT INTO track(id,name,length,album_id)
                       VALUES ({track_id},'{track_title}','{track_length}',{album_id})
                       ON CONFLICT (id) DO UPDATE 
                            SET name = excluded.name, 
                                length = excluded.length,
                                album_id = excluded.album_id;

                       INSERT INTO TrackCollection(track_id,collection_id)
                       VALUES ({track_id},'{id_radio}')
                       ON CONFLICT (track_id,collection_id) DO UPDATE 
                            SET track_id = excluded.track_id, 
                                collection_id = excluded.collection_id;
                       
                       INSERT INTO AlbumSinger(singer_id,album_id)
                       VALUES ({singer_id},'{album_id}')
                       ON CONFLICT (singer_id,album_id) DO UPDATE 
                            SET singer_id = excluded.singer_id, 
                                album_id = excluded.album_id;

                       INSERT INTO sstyle(id,name)
                       VALUES ({style_id},'{style_name}')
                       ON CONFLICT (id) DO UPDATE 
                            SET name = excluded.name;

                       INSERT INTO StyleSinger(sstyle_id, singer_id)
                       VALUES ({style_id},{singer_id})
                       ON CONFLICT (sstyle_id, singer_id) DO UPDATE 
                            SET singer_id = excluded.singer_id, 
                                sstyle_id = excluded.sstyle_id;
                       """
        )
        print(f"Добавлена песня {track_title} : {singer_name}")
    return

engine = sqlalchemy.create_engine('postgresql://netology:pass@localhost:5432/singer_new')
connection = engine.connect()

dict_collection ={}

# Insert_from_top_radio(dict_collection, limit=16)
get_topradio(dict_collection,18)

for key in dict_collection.keys():
    Insert_from_radio(key, 10)

