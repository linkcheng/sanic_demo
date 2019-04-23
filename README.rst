===============================
bi-open
===============================

Quickstart
----------

Run the following commands to bootstrap your environment ::

    cd bi-open
    pipenv install --dev   # if error, try: pipenv run pip install pip==18.0
    cp .env.example .env


In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``.


Check
-----

To check the system is running ::

    1. "It works." will get when access http://127.0.0.1:5000/ .
    2. If "SENTRY_DSN" is configured in ".env" file, when access http://127.0.0.1:5000/error , there will raise an error and send a notification to sentry system.

