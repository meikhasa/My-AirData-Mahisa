from flask import Blueprint, jsonify
from controllers.surabaya_utara_controller.utara_openmateo_controller import pollutant_openmateo as utara_ctrl, weather_openmateo
from controllers.surabaya_utara_controller.utara_nasapower_controller import column_nasapower as utara_nasa_ctrl
from controllers.controller_view.dashboard_controller import get_normalized_data

utara_bp = Blueprint("surabaya_utara", __name__)

@utara_bp.route("/surabaya_utara_normalisasi")
def get_surabaya_utara_normalisasi():
    return get_normalized_data(utara_ctrl, "Surabaya Utara")

@utara_bp.route("/surabaya_utara_nasa")
def get_surabaya_utara_nasa():
    return utara_nasa_ctrl.fetch_data_nasapower()

@utara_bp.route("/surabaya_utara_weather")
def get_surabaya_utara_weather():
    res = weather_openmateo.fetch_weather_utara()
    return jsonify(res)