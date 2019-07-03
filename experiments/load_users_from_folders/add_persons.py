
import base64
import os
import sys
from urllib.parse import urljoin

import PIL
import face_recognition
import requests
from face_recognition.face_recognition_cli import image_files_in_folder

app_base_url = None

def iterate_persons(persons_source_dir):

    # Loop through each person in the training set
    for person_dir in os.listdir(persons_source_dir):
        if not os.path.isdir(os.path.join(persons_source_dir, person_dir)):
            continue

        print(person_dir)

        # TODO make request to create person.
        response = requests.post(urljoin(app_base_url, 'users'), json={'name': person_dir})

        created_person = response.json()

        print(created_person)

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(persons_dir, person_dir)):
            print(img_path)

            with open(img_path, 'rb') as image:
                response = requests.post(urljoin(app_base_url, 'users/{}/photos'.format(created_person['id'])), json={'data': base64.b64encode(image.read()).decode()})

            print('create photo {}'.format(str(response)))




if __name__ == '__main__':

    # app_base_url = sys.argv[1]

    # persons_dir = sys.argv[2]

    app_base_url = 'http://localhost:5000'

    persons_dir = './'

    iterate_persons(persons_dir)
