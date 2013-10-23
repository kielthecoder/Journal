DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR,
	email VARCHAR,
	password VARCHAR
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	author_id INTEGER REFERENCES users (id),
	posted TIMESTAMP,
	body TEXT,
	slug TEXT
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR
);

DROP TABLE IF EXISTS tags_to_posts;
CREATE TABLE tags_to_posts (
	tag_id INTEGER REFERENCES tags (id),
	post_id INTEGER REFERENCES posts (id)
);

INSERT INTO users (name,email,password) VALUES
	("Kiel","kiel.lofstrand@gmail.com","password");
INSERT INTO users (name,email,password) VALUES
	("Brittany","brit0000@hotmail.com","password");

INSERT INTO posts (title,author_id,posted,body,slug) VALUES
	("My First Post",1,DATETIME("2013-10-18 12:00:00"),
"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	 "my-first-post.html");

INSERT INTO tags (name) VALUES ("testing");
INSERT INTO tags_to_posts (tag_id,post_id) VALUES (1,1);

INSERT INTO posts (title,author_id,posted,body,slug) VALUES
	("My Second Post",1,DATETIME("2013-10-20 12:00:00"),
"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	 "my-second-post.html");

INSERT INTO tags (name) VALUES ("uncategorized");
INSERT INTO tags_to_posts (tag_id,post_id) VALUES (1,2);
INSERT INTO tags_to_posts (tag_id,post_id) VALUES (2,2);

