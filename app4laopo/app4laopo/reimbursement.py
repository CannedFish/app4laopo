# -*- coding: utf-8 -*-
import json
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort, current_app
)
from werkzeug.exceptions import abort

from app4laopo.auth import login_required
from app4laopo.db import get_db

bp = Blueprint('reimbursement', __name__, url_prefix='/reimbursement')
ENDPOINT = "http://127.0.0.1:9091/api/v1"


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    # db = get_db()
    # posts = db.execute(
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('reimbursement/reimbursement.html')

@bp.route('/hospital', methods=('GET', 'POST'))
# @login_required
def hospitals():
    url = ENDPOINT + '/hospital/'
    if request.method == 'GET':
        res = requests.get(url)
        current_app.logger.debug(res.text)
        return res.text
    elif request.method == 'POST':
        current_app.logger.debug(request.data)
        h = json.loads(request.data)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {"hospitals": [h]}
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        return res.text, 201
    else:
        abort(405)

@bp.route('/location', methods=('GET', ))
# @login_required
def location():
    h_name = request.args.get('name', '')
    payload = {'name': h_name}
    res = requests.get(ENDPOINT+'/location/', params=payload)
    current_app.logger.debug(res.text)
    return res.text

@bp.route('/hospital/<string:id>', methods=('GET', 'PUT', 'DELETE'))
# @login_required
def hospital(id):
    url = ENDPOINT + '/hospital/%s/' % id
    if request.method == 'GET':
        current_app.logger.debug("GET: %s" % id)
        res = requests.get(url)
        return res.text, res.status_code
    elif request.method == 'PUT':
        current_app.logger.debug("PUT update: %s" % request.data)
        headers = {'Content-Type': 'application/json'}
        res = requests.put(url, data=request.data, headers=headers)
        return res.text, res.status_code
    else:
        current_app.logger.debug("DELETE: %s" % id)
        res = requests.delete(url)
        return res.text, res.status_code

@bp.route('/distance', methods=('GET', ))
# @login_required
def distance():
    target = request.args.get('target', 20)
    h_id = request.args.get('id', '')
    end_type = request.args.get('type', 'src')
    current_app.logger.debug("target: %s, name: %s, type: %s" % (target, h_id, end_type))
    payload = {
        'target': target,
        end_type: h_id
    }
    res = requests.get(ENDPOINT+'/distance/', params=payload)
    return res.text, res.status_code

# # TODO: remove
# def get_post(id, check_author=True):
    # """Get a post and its author by id.

    # Checks that the id exists and optionally that the current user is
    # the author.

    # :param id: id of post to get
    # :param check_author: require the current user to be the author
    # :return: the post with author information
    # :raise 404: if a post with the given id doesn't exist
    # :raise 403: if the current user isn't the author
    # """
    # post = get_db().execute(
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' WHERE p.id = ?',
        # (id,)
    # ).fetchone()

    # if post is None:
        # abort(404, "Post id {0} doesn't exist.".format(id))

    # if check_author and post['author_id'] != g.user['id']:
        # abort(403)

    # return post


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
    # """Create a new post for the current user."""
    # if request.method == 'POST':
        # title = request.form['title']
        # body = request.form['body']
        # error = None

        # if not title:
            # error = 'Title is required.'

        # if error is not None:
            # flash(error)
        # else:
            # db = get_db()
            # db.execute(
                # 'INSERT INTO post (title, body, author_id)'
                # ' VALUES (?, ?, ?)',
                # (title, body, g.user['id'])
            # )
            # db.commit()
            # return redirect(url_for('blog.index'))

    # return render_template('blog/create.html')


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
    # """Update a post if the current user is the author."""
    # post = get_post(id)

    # if request.method == 'POST':
        # title = request.form['title']
        # body = request.form['body']
        # error = None

        # if not title:
            # error = 'Title is required.'

        # if error is not None:
            # flash(error)
        # else:
            # db = get_db()
            # db.execute(
                # 'UPDATE post SET title = ?, body = ? WHERE id = ?',
                # (title, body, id)
            # )
            # db.commit()
            # return redirect(url_for('blog.index'))

    # return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
    # """Delete a post.

    # Ensures that the post exists and that the logged in user is the
    # author of the post.
    # """
    # get_post(id)
    # db = get_db()
    # db.execute('DELETE FROM post WHERE id = ?', (id,))
    # db.commit()
    # return redirect(url_for('blog.index'))
