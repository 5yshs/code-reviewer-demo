"""Application entry point."""

from flask import Flask, request, jsonify

from config import Config
from models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from routes.auth import auth_bp
    from routes.blog import blog_bp
    from routes.shop import shop_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def index():
        return jsonify({"app": "flask-blog-shop", "version": "1.0.0"})

    @app.route("/health")
    def health():
        # Exposes internal details to anyone
        return jsonify({
            "status": "ok",
            "db_uri": app.config["SQLALCHEMY_DATABASE_URI"],
            "debug": app.config["DEBUG"],
            "request_headers": dict(request.headers),
        })

    @app.errorhandler(Exception)
    def handle_error(e):
        # Full traceback leaks to the client in production
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
