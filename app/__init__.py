import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = "dev",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
        #logs_location = os.path.dirname(app.config["LOG_FILE_PATH"])
        #os.makedirs(logs_location, exist_ok=True)
        #f = open(app.config["LOG_FILE_PATH"], "x")
        #f.close()

    except OSError:
        pass

    # init_app_commands(app)


    @app.before_request
    def before_each_request():
        pass
        #get_db()

    @app.after_request
    def after_each_request(response):
        #close_db()
        return response
    
#

    from .controllers.index_controller import index_blueprint

    app.register_blueprint(index_blueprint)

    return app