# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from werkzeug.utils import find_modules, import_string
from sanic import Sanic
from sanic_sentry import SanicSentry

from . import settings
from .utils.sanicdb import SanicDB
from .utils.log import configure_logging


def create_app(config_object=settings):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Sanic(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_config(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db_config = app.config.DB_CONFIG.get('DB_CONFIG')
    SanicDB(**db_config, sanic=app)
    SanicSentry(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    for name in find_modules('app.routes'):
        mod = import_string(name)
        if hasattr(mod, 'public_pb'):
            app.register_blueprint(mod.public_pb)
        if hasattr(mod, 'greylist_pb'):
            app.register_blueprint(mod.greylist_pb)

    return None


def register_config(app):
    """Register config"""
    configure_logging()
