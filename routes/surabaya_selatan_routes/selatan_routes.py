from flask import Blueprint, jsonify
from controllers.surabaya_selatan_controller.selatan_openmateo_controller import pollutant_openmateo as selatan_ctrl, weather_openmateo
from controllers.surabaya_selatan_controller.selatan_nasapower_controller import column_nasapower as selatan_nasa_ctrl
from controllers.controller_view.dashboard_controller import get_normalized_data

selatan_bp = Blueprint("surabaya_selatan", __name__)

@selatan_bp.route("/surabaya_selatan_normalisasi")
def get_surabaya_selatan_normalisasi():
    return get_normalized_data(selatan_ctrl, "Surabaya Selatan")

@selatan_bp.route("/surabaya_selatan_nasa")
def get_surabaya_selatan_nasa():
    return selatan_nasa_ctrl.fetch_data_nasapower()

@selatan_bp.route("/surabaya_selatan_weather")
def get_surabaya_selatan_weather():
    res = weather_openmateo.fetch_weather_selatan()
    return jsonify(res)