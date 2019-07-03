import base64
import re

import numpy as np

import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from flask import Flask, request, jsonify

known_face_encodings = list()
known_face_names = list()

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


def predict(photo_data):

    # Load image file and find face locations
    img = bytes_to_image(photo_data)

    face_locations = timeit(face_recognition.face_locations)(img, model='hog')
    face_encodings = timeit(face_recognition.face_encodings)(img, face_locations)

    # If no faces are found in the image, return an empty result.
    if len(face_encodings) == 0:
        return []

    persons = list()

    # Loop through each face in this frame of video
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = timeit(face_recognition.compare_faces)(known_face_encodings, face_encoding)

        name = "unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        persons.append(name)

    return {
        'unknown_persons_count': persons.count("unknown"),
        'known_persons': list(filter(lambda x: x != "unknown", persons))
    }

def bytes_to_image(photo_data):
    import io
    return face_recognition.load_image_file(io.BytesIO(photo_data))


def add_known_person(name, image_path):
    image = face_recognition.load_image_file(image_path)
    person_face_encoding = face_recognition.face_encodings(image)[0]

    known_face_encodings.append(person_face_encoding)
    known_face_names.append(name)


if __name__ == '__main__':

    # TODO see the persons folder and train
    for img_path in image_files_in_folder('./persons'):
        print(re.search('./persons/(.+?)-1\.jp.*', img_path).group(1))
        add_known_person(re.search('./persons/(.+?)-1\.jp.*', img_path).group(1), img_path)


    app.run()

