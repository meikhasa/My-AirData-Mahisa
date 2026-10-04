from flask import Blueprint, jsonify
from controllers.surabaya_timur_controller.timur_openmateo_controller import pollutant_openmateo as timur_ctrl, weather_openmateo
from controllers.surabaya_timur_controller.timur_nasapower_controller import column_nasapower as timur_nasa_ctrl
from controllers.controller_view.dashboard_controller import get_normalized_data

timur_bp = Blueprint("surabaya_timur", __name__)

@timur_bp.route("/surabaya_timur_normalisasi")
def get_surabaya_timur_normalisasi():
    return get_normalized_data(timur_ctrl, "Surabaya Timur")

@timur_bp.route("/surabaya_timur_nasa")
def get_surabaya_timur_nasa():
    return timur_nasa_ctrl.fetch_data_nasapower()

@timur_bp.route("/surabaya_timur_weather")
def get_surabaya_timur_weather():
    res = weather_openmateo.fetch_weather_timur()
    return jsonify(res)