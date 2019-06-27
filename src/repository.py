from src import db
from src.models import User, Photo
from src.recognition import update_classifier, validate_photo_data


def get_all_users():
    return User.query.all()


def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


def create_user(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return user

@update_classifier
def update_user(user_id, new_user_name):
    user_to_update = get_user(user_id)
    user_to_update.name = new_user_name
    db.session.commit()
    return user_to_update


@update_classifier
def delete_user(user_id):
    user_to_delete = get_user(user_id)
    Photo.query.filter_by(user_id=user_id).delete()
    db.session.delete(user_to_delete)
    db.session.commit()
    return user_to_delete


def get_user_photos(user_id):
    return Photo.query.filter_by(user_id=user_id).all()


@validate_photo_data
@update_classifier
def create_photo(user_id, photo_data):
    photo = Photo(user_id=user_id, data=photo_data)
    db.session.add(photo)
    db.session.commit()
    return photo

@update_classifier
def delete_photo(photo_id):
    photo_to_delete = Photo.query.filter_by(id=photo_id).first()
    db.session.delete(photo_to_delete)
    db.session.commit()
    return photo_to_delete




