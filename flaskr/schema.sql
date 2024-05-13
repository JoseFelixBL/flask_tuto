/*
 DROP TABLE IF EXISTS user;
 DROP TABLE IF EXISTS post;
 */
DROP TABLE IF EXISTS post_like;
DROP VIEW IF EXISTS v_total_likes;
CREATE TABLE IF NOT EXISTS user (
    id INTEGER primary key autoincrement,
    username Text unique not null,
    password text not null
);
CREATE TABLE IF NOT EXISTS post (
    id INTEGER primary key autoincrement,
    author_id INTEGER not null,
    created timestamp not null default CURRENT_TIMESTAMP,
    title text not null,
    body text not null,
    foreign key (author_id) references user (id)
);
CREATE TABLE IF NOT EXISTS post_like (
    /* id INTEGER PRIMARY KEY autoincrement, */
    post_id INTEGER not null,
    author_id INTEGER not null,
    PRIMARY KEY(post_id, author_id),
    foreign KEY (post_id) references post (id),
    foreign KEY (author_id) references user (id)
);
CREATE VIEW IF NOT EXISTS v_total_likes (post_id, n_likes) AS
SELECT post_id,
    COUNT(post_id)
FROM post_like
GROUP BY post_id