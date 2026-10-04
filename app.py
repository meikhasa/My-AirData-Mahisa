from flask import Flask
from routes.routes_view.view_routes import view_bp
from routes.surabaya_pusat_routes.pusat_routes import pusat_bp
from routes.surabaya_utara_routes.utara_routes import utara_bp
from routes.surabaya_selatan_routes.selatan_routes import selatan_bp
from routes.surabaya_timur_routes.timur_routes import timur_bp
from routes.surabaya_barat_routes.barat_routes import barat_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(view_bp)
app.register_blueprint(pusat_bp)
app.register_blueprint(utara_bp)
app.register_blueprint(selatan_bp)
app.register_blueprint(timur_bp)
app.register_blueprint(barat_bp)

if __name__ == "__main__":
    app.run(debug=True)