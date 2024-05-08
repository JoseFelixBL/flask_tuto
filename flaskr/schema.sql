DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
CREATE TABLE user (
    id INTEGER primary key autoincrement,
    username Text unique not null,
    password text not null
);
CREATE TABLE post (
    id INTEGER primary key autoincrement,
    author_id INTEGER not null,
    created timestamp not null default CURRENT_TIMESTAMP,
    title text not null,
    body text not null,
    foreign key (author_id) references user (id)
);