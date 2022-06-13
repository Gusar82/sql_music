--1. Количество исполнителей в каждом жанре--
SELECT ss.name, count(st.sstyle_id) count_st FROM sstyle ss
JOIN stylesinger st ON ss.id = st.sstyle_id 
GROUP BY ss.id
ORDER BY count_st;

--2. Количество треков вошедших в альбомы 2019-2020 годов--
SELECT a.title, count(t.id) count FROM album a 
LEFT JOIN track t ON t.album_id = a.id
WHERE EXTRACT (YEAR FROM release_year) BETWEEN 2019 AND 2020
GROUP BY a.id 
ORDER BY count DESC; 

--3. средняя продолжительность треков по каждому альбому--
SELECT a.title, AVG(t.length) middle, count(t.length) count FROM album a 
LEFT JOIN track t ON t.album_id = a.id
GROUP BY a.id 
ORDER BY middle; 

-- 4. все исполнители, которые не выпустили альбомы в 2020 году;
SELECT DISTINCT s.id, s.name FROM singer s 
LEFT JOIN albumsinger a ON a.singer_id = s.id 
LEFT JOIN album a2 ON (a2.id = a.album_id)
WHERE s.id  NOT IN (SELECT DISTINCT s.id FROM singer s 
			  		JOIN albumsinger a ON a.singer_id = s.id 
			  		JOIN album a2 ON a2.id = a.album_id
			  		WHERE EXTRACT (YEAR FROM release_year) = 2020)
ORDER BY s.id; 

-- 5. названия сборников, в которых присутствует конкретный исполнитель (Adele)
SELECT c.title FROM collection c
JOIN trackcollection t ON t.collection_id = c.id 
JOIN track t2 ON t2.id = t.track_id 
JOIN album a ON a.id = t2.album_id 
JOIN albumsinger a2 ON a2.album_id = a.id 
JOIN singer s ON (s.id = a2.singer_id) AND (s.name = 'Adele'); 

-- 6. название альбомов, в которых присутствуют исполнители более 1 жанра
SELECT DISTINCT a.title FROM album a 
JOIN albumsinger a2 ON a2.album_id = a.id
WHERE a2.singer_id IN (SELECT s.id FROM singer s 
					  JOIN stylesinger s2 ON s2.singer_id = s.id
					  GROUP BY s.id
					  HAVING count(s2.sstyle_id)>1)	
ORDER BY a.title;

-- 7. Наименование треков, которые не входят в сборники
SELECT name FROM track t 
LEFT JOIN trackcollection t2 ON t2.track_id = t.id
WHERE t2.collection_id IS NULL;

-- 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько)
SELECT t.length, s.name FROM track t
JOIN album a ON a.id = t.album_id
JOIN albumsinger a2 ON a2.album_id = a.id 
JOIN singer s ON s.id = a2.singer_id
WHERE length = (SELECT min(length) FROM track);

-- 8. ИЛИ
SELECT s.name  FROM singer s
WHERE s.id IN (SELECT DISTINCT singer_id FROM albumsinger al
			   WHERE al.album_id IN (SELECT DISTINCT t.album_id FROM track t
				     				 WHERE t.length = (SELECT min(length) FROM track)));

-- 9. название альбомов, содержащих наименьшее количество треков
SELECT a.title, count(t.id) FROM album a 
LEFT JOIN track t ON t.album_id = a.id
GROUP BY a.id
HAVING COUNT(t.id) = (SELECT count(id) count FROM track
					  GROUP BY album_id
					  ORDER BY count
					  LIMIT 1)
ORDER BY a.title; 



