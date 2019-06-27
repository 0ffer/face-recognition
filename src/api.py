"""
Rest service to recognize known people by photo.
"""
import base64

from flask import Blueprint, request, jsonify

import src.repository as repo

bp = Blueprint("main", __name__)

# For readable errors in console need comment this error handler
@bp.errorhandler(Exception)
def on_error(e):
    return str(e), 400


@bp.route('/users', methods = ['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(repo.get_all_users())

    if request.method == 'POST':
        content = request.get_json()
        return jsonify(repo.create_user(content['name'])), 201


@bp.route('/users/<int:user_id>', methods = ['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        return jsonify(repo.get_user(user_id))

    if request.method == 'PUT':
        content = request.get_json()
        return jsonify(repo.update_user(user_id, content['name']))

    if request.method == 'DELETE':
        return jsonify(repo.delete_user(user_id))


@bp.route('/users/<int:user_id>/photos', methods = ['GET', 'POST'])
def user_photos(user_id):
    if request.method == 'GET':
        return jsonify(repo.get_user_photos(user_id))

    if request.method == 'POST':
        content = request.get_json()
        photo_data = base64.b64decode(content['data'])
        return jsonify(repo.create_photo(user_id, photo_data))


@bp.route('/photos/<int:photo_id>', methods = ['DELETE'])
def delete_photo(photo_id):
    return jsonify(repo.delete_photo(photo_id))


def timeit(method):
    def timed(*args, **kw):
        import time
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


@bp.route('/users/recognize', methods = ['POST'])
@timeit
def recognize_user_by_photo():
    """
    Recognize users by photo.
    It return unknown people count too.
    """
    content = request.get_json()
    photo_data = base64.b64decode(content['data'])

    import src.recognition as recognition
    return jsonify(recognition.predict(photo_data))
