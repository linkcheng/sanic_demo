# -*- coding: utf-8 -*-
"""Create an application instance."""
# gunicorn -w 4 --timeout 100 -b 0.0.0.0:40000  --worker-class sanic.worker.GunicornWorker wsgi:app
from app.app import create_app

app = create_app()


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=True)
