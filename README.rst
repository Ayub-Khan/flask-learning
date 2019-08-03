================
Flask Learning
================

.. image:: https://circleci.com/gh/Ayub-Khan/flask-learning/tree/master.svg?style=svg
        :target: https://circleci.com/gh/Ayub-Khan/flask-learning


Flask Learning is a learning/practise repo.

Features
--------
The App have the following features

* Integrated Circleci Quality tests
* pipenv for dependency management
* Flask Rest Apis example
* Flask Basic Authentication
* Flask Encrypted Responses

Local Setup
--------
Run the following commands to setup project locally.

* Create the virtualenv

   make create-venv

* Install the dependencies

   make requirements

* Activate the virtualenv

   make venv

* Run the server

   make server

Additional Features
--------

* by default the encryption is not active set ENABLE_ENCRIPTION = True to activate
* Use postman collection export file flask-learning-rest-apis.postman_collection.json for testing.
