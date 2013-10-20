DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR,
	email VARCHAR,
	password VARCHAR
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	id INTEGER PRIMARY KEY,
	title TEXT,
	author_id INTEGER REFERENCES users (id),
	posted TIMESTAMP,
	body TEXT,
	slug TEXT
);

INSERT INTO users (name,email,password) VALUES
	("Kiel","kiel.lofstrand@gmail.com","password");
INSERT INTO users (name,email,password) VALUES
	("Brittany","brit0000@hotmail.com","password");

INSERT INTO posts (title,author_id,posted,body,slug) VALUES
	("My First Post",1,DATETIME("now"),
"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	 "my-first-post.html");
