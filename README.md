# face-recognition
Some tests and examples

## Local run

1. init venv

To run app need next command
```FLASK_APP=src flask run```

## Data structure

There is 2 simple entity in application
* user (id:int, name:string)
* photo (id:int, user_id:int, data:bytes)

Photo "data" field send to server in Base64 format.

Some endpoints:
* /users
    * GET - get all users
    * POST - create user (in request body "name" field required)
* /users/<int: user_id>
    * GET - get single user with specified id
    * PUT - update user (in request body "name" field required)
    * DELETE - delete user with cpecified id
* /users/<int: user_id>/photos
    * GET - get all user photos
    * POST - add photo to user (in request body "data" field required)
* /photos/<int: photo_id>
    * DELETE - deletes photo with specified identifier
* /users/recognize
    * POST - recognize users on photo (in request body "data" field required)

The response on recognize request have next view:
{
"unknown_persons_count":0
"known_persons":["trump"],
}
