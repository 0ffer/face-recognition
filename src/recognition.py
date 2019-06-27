"""
Face recognition service
"""

import math
from functools import wraps

import face_recognition
from sklearn import neighbors

classifier = None


def train(users, n_neighbors=None, knn_algo='ball_tree'):
    """
    Train classifier on data from database
    :param n_neighbors:
    :param knn_algo:
    :return:
    """

    X = []
    y = []

    for user in users:
        for photo in user.photos:
            image = bytes_to_image(photo.data)
            face_bounding_boxes = face_recognition.face_locations(image)

            X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            y.append(user.name)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        print("Chose n_neighbors automatically:", n_neighbors)

    if not X or not y:
        return None

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    return knn_clf


def predict(photo_data, distance_threshold=0.6):

    if not classifier:
        return None

    # Load image file and find face locations
    img = bytes_to_image(photo_data)
    face_locations = face_recognition.face_locations(img)

    # If no faces are found in the image, return an empty result.
    if len(face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(img, known_face_locations=face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = classifier.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    persons = [pred if rec else "unknown" for pred, rec in zip(classifier.predict(faces_encodings), are_matches)]

    return {
        'unknown_persons_count': persons.count("unknown"),
        'known_persons': list(filter(lambda x: x != "unknown", persons))
    }


def bytes_to_image(photo_data):
    import io
    return face_recognition.load_image_file(io.BytesIO(photo_data))


def validate_photo_data(func):
    """
    Photo data validation.
    It check:
    1. We can understand the image
    2. In only one face on image
    """
    @wraps(func)
    def wrapper_validate_photo_data(*args, **kwargs):

        photo_data = args[1]
        image = bytes_to_image(photo_data)
        face_bounding_boxes = face_recognition.face_locations(image)

        if len(face_bounding_boxes) != 1:
            raise Exception("Image not suitable for training: {}".format("Didn't find a face" if len(
                face_bounding_boxes) < 1 else "Found more than one face"))

        return func(*args, **kwargs)

    return wrapper_validate_photo_data


def update_context():
    import src.repository as repo
    global classifier
    classifier = train(repo.get_all_users())
    print('Classifyer updates successfully!')


def update_classifier(func):
    """
    Decorator to update classifier state.

    Use when method change some use data.
    :param func: Function that change some user data.
    """
    @wraps(func)
    def wrapper_update_classifier(*args, **kwargs):
        res = func(*args, **kwargs)

        update_context()

        return res

    return wrapper_update_classifier
