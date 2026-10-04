from flask import Blueprint, jsonify
from controllers.surabaya_barat_controller.barat_openmateo_controller import pollutant_openmateo as barat_ctrl, weather_openmateo
from controllers.surabaya_barat_controller.barat_nasapower_controller import column_nasapower as barat_nasa_ctrl
from controllers.controller_view.dashboard_controller import get_normalized_data

barat_bp = Blueprint("surabaya_barat", __name__)

@barat_bp.route("/surabaya_barat_normalisasi")
def get_surabaya_barat_normalisasi():
    return get_normalized_data(barat_ctrl, "Surabaya Barat")

@barat_bp.route("/surabaya_barat_nasa")
def get_surabaya_barat_nasa():
    return barat_nasa_ctrl.fetch_data_nasapower()

@barat_bp.route("/surabaya_barat_weather")
def get_surabaya_barat_weather():
    res = weather_openmateo.fetch_weather_barat()
    return jsonify(res)