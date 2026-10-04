from flask import Blueprint, jsonify
from controllers.surabaya_pusat_controller.pusat_openmateo_controller import pollutant_openmateo as pusat_ctrl, weather_openmateo
from controllers.surabaya_pusat_controller.pusat_nasapower_controller import column_nasapower as pusat_nasa_ctrl
from controllers.controller_view.dashboard_controller import get_normalized_data

pusat_bp = Blueprint("surabaya_pusat", __name__)

@pusat_bp.route("/surabaya_pusat_normalisasi")
def get_surabaya_pusat_normalisasi():
    return get_normalized_data(pusat_ctrl, "Surabaya Pusat")

@pusat_bp.route("/surabaya_pusat_nasa")
def get_surabaya_pusat_nasa():
    return pusat_nasa_ctrl.fetch_data_nasapower()

@pusat_bp.route("/surabaya_pusat_weather")
def get_surabaya_pusat_weather():
    res = weather_openmateo.fetch_weather_pusat()
    return jsonify(res)