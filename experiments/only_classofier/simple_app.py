import base64
import pickle

import face_recognition
from flask import Flask, request, jsonify

classifier = None

app = Flask(__name__)

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


@app.route('/users/recognize', methods = ['POST'])
@timeit
def predict():
    content = request.get_json()
    photo_data = base64.b64decode(content['data'])

    return jsonify(predict(photo_data))

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

if __name__ == '__main__':

    # global classifier
    with open('classifier.clf', 'rb') as f:
        # global classifier
        classifier = pickle.load(f)
    # classifier = pickle.load(open('classifier.clf', 'rb'))

    app.run()


