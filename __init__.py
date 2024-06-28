from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    oauth.init_app(app)
    app.register_blueprint(auth)

    return app
