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
ENDPOINT = "http://127.0.0.1:5000/api/v1"


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

TEST_DATA = [{"name_ch":"甲医院","lng":0,"address":"甲路1号","lat":0,"name_en":"Hospital Jia","id":"33928d323"},{"name_ch":"乙医院","lng":0,"address":"乙路1号","lat":0,"name_en":"Hospital Yi","id":"33928d320"},{"name_ch":"丙医院","lng":0,"address":"丙路1号","lat":0,"name_en":"Hospital Bing","id":"33958d320"},{"name_ch":"丁医院","lng":0,"address":"丁路1号","lat":0,"name_en":"Hospital Ding","id":"33998d320"}]

@bp.route('/hospital', methods=('GET', 'POST'))
# @login_required
def hospitals():
    if request.method == 'GET':
        res = requests.get(ENDPOINT+'/hospital/')
        current_app.logger.debug(res.text)
        return json.dumps(TEST_DATA)
    elif request.method == 'POST':
        current_app.logger.debug(request.data)
        h = json.loads(request.data)
        h['id'] = "3x928d323"
        h['name_en'] = ""
        TEST_DATA.append(h)
        return json.dumps(h), 201
    else:
        abort(405)

TEST_DATA2 = [{"name_ch":"甲医院2","lng":0,"address":"甲2路1号","lat":0},{"name_ch":"乙医院2","lng":0,"address":"乙2路1号","lat":0},{"name_ch":"丙医院2","lng":0,"address":"丙2路1号","lat":0},{"name_ch":"丁医院2","lng":0,"address":"丁2路1号","lat":0}]

@bp.route('/location', methods=('GET', ))
# @login_required
def location():
    h_name = request.args.get('name', '')
    current_app.logger.debug(h_name)
    return json.dumps(TEST_DATA2)

@bp.route('/hospital/<string:id>', methods=('GET', 'PUT', 'DELETE'))
# @login_required
def hospital(id):
    if request.method == 'GET':
        current_app.logger.debug("GET: %s" % id)
        return 200
    elif request.method == 'PUT':
        current_app.logger.debug("PUT update: %s" % request.data)
        return request.data, 200
    else:
        current_app.logger.debug("DELETE: %s" % id)
        return 200

TEST_DATA3 = [{"src":{"name_ch":"甲医院","lng":0,"address":"","lat":0,"name_en":"Hospital Jia","id":"33928d120"},"dst":{"name_ch":"乙医院","lng":0,"address":"","lat":0,"name_en":"Hospital Yi","id":"33928d320"},"distance":"24"},{"src":{"name_ch":"甲医院","lng":0,"address":"","lat":0,"name_en":"Hospital Jia","id":"33928d120"},"dst":{"name_ch":"乙医院","lng":0,"address":"","lat":0,"name_en":"Hospital Yi","id":"33928d320"},"distance":"25"},{"src":{"name_ch":"甲医院","lng":0,"address":"","lat":0,"name_en":"Hospital Jia","id":"33928d120"},"dst":{"name_ch":"乙医院","lng":0,"address":"","lat":0,"name_en":"Hospital Yi","id":"33928d320"},"distance":"28"}]

@bp.route('/distance', methods=('GET', ))
# @login_required
def distance():
    target = request.args.get('target', '20')
    h_name = request.args.get('name', '')
    end_type = request.args.get('type', 'src')
    current_app.logger.debug("target: %s, name: %s, type: %s" % (target, h_name, end_type))
    return json.dumps(TEST_DATA3)

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
