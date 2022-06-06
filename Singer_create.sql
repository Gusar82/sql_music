CREATE TABLE IF NOT EXISTS sstyle (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS singer (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS stylesinger (
	sstyle_id INTEGER REFERENCES sstyle(id),
	singer_id INTEGER REFERENCES singer(id),
	CONSTRAINT stylesinger_pk PRIMARY KEY (sstyle_id, singer_id)
);

CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL,
	release_year DATE
);

CREATE TABLE IF NOT EXISTS albumsinger (
	album_id INTEGER REFERENCES album(id),
	singer_id INTEGER REFERENCES singer(id),
	CONSTRAINT albumsinger_pk PRIMARY KEY (album_id, singer_id)
);

CREATE TABLE IF NOT EXISTS track (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	length INTERVAL SECOND,
	album_id INTEGER NOT NULL REFERENCES album(id)
);

CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	title VARCHAR(40) NOT NULL,
	release_year DATE
);
CREATE TABLE IF NOT EXISTS trackcollection (
	track_id INTEGER REFERENCES track(id),
	collection_id INTEGER REFERENCES collection(id),
	CONSTRAINT trackcollection_pk PRIMARY KEY (track_id, collection_id)
);