"""Blog Blueprint"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Index: list of posts"""
    db = get_db()
    # 'SELECT p.id, title, body, created, author_id, username'
    # ' FROM post p JOIN user u ON p.author_id = u.id'
    # ' ORDER BY created DESC'
    if g.user == None:
        posts = db.execute(
            """SELECT p.id, title, body, created, p.author_id, 
                username, n_likes
                FROM post p
                LEFT JOIN post_like pl ON p.id = pl.post_id
                JOIN user u ON p.author_id = u.id
                LEFT JOIN v_total_likes vtl ON p.id = vtl.post_id
                GROUP BY p.id"""
        ).fetchall()
    else:
        posts = db.execute(
            """SELECT p.id, title, body, created, p.author_id, 
                username, n_likes, pl.author_id pl_auth
                FROM post p
                LEFT JOIN post_like pl ON p.id = pl.post_id and pl.author_id = ?
                JOIN user u ON p.author_id = u.id
                LEFT JOIN v_total_likes vtl ON p.id = vtl.post_id""", (g.user['id'],)
        ).fetchall()
    # posts=db.execute(
    #     'SELECT p.id, title, body, created, author_id, username, n_likes'
    #     ' FROM post p'
    #     ' JOIN user u ON p.author_id = u.id'
    #     ' LEFT JOIN v_total_likes ON p.id = post_id'
    # ).fetchall()
    print(g.user)
    return render_template('blog/index.html', posts=posts)


@ bp.route('/create', methods=('GET', 'POST'))
@ login_required
def create():
    """Create a new post"""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """Get post by id, check_author in case of update or delete"""
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@ bp.route('/<int:id>/update', methods=('GET', 'POST'))
@ login_required
def update(id):
    """Update post"""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@ bp.route('/<int:id>/detail', methods=('GET',))
def detail(id):
    """Detail post"""
    post = get_post(id, check_author=False)
    return render_template('blog/detail.html', post=post)


@ bp.route('/<int:id>/delete', methods=('POST',))
@ login_required
def delete(id):
    """Delete post"""
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
