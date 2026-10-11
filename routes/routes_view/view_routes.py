import random
from flask import Blueprint, jsonify, render_template
from controllers.controller_view.dashboard_controller import load_mock_data

# Import normalisasi polutan per daerah
from routes.surabaya_pusat_routes.pusat_routes import get_surabaya_pusat_normalisasi
from routes.surabaya_utara_routes.utara_routes import get_surabaya_utara_normalisasi
from routes.surabaya_selatan_routes.selatan_routes import get_surabaya_selatan_normalisasi
from routes.surabaya_timur_routes.timur_routes import get_surabaya_timur_normalisasi
from routes.surabaya_barat_routes.barat_routes import get_surabaya_barat_normalisasi

# Import controller cuaca Open-Meteo dari masing-masing daerah
from controllers.surabaya_pusat_controller.pusat_openmateo_controller import weather_openmateo as pusat_weather
from controllers.surabaya_utara_controller.utara_openmateo_controller import weather_openmateo as utara_weather
from controllers.surabaya_selatan_controller.selatan_openmateo_controller import weather_openmateo as selatan_weather
from controllers.surabaya_timur_controller.timur_openmateo_controller import weather_openmateo as timur_weather
from controllers.surabaya_barat_controller.barat_openmateo_controller import weather_openmateo as barat_weather

view_bp = Blueprint("view_routes", __name__)

@view_bp.route("/")
def index():
    try:
        res = get_surabaya_pusat_normalisasi()
        norm_data = res.get_json()

        if norm_data and norm_data.get("status") == "success":
            converted = norm_data.get("ispu_converted", {})
            air_data = {
                "co": converted.get("CO"),
                "no2": converted.get("NO2"),
                "pm25": converted.get("PM25"),
                "pm10": converted.get("PM10"),
                "o3": converted.get("O3"),
                "so2": converted.get("SO2"),
            }
        else:
            air_data = {}
    
        return render_template("index.html", air=air_data, air_quality=air_data)
    except Exception as e:
        return render_template("index.html", air={}, air_quality={})
    

@view_bp.route("/api/dashboard/<location_id>", methods=["GET"])
def get_dashboard_data(location_id):
    try:
        mock_data = load_mock_data()
        data = mock_data.get(location_id, mock_data.get("surabaya_pusat"))

        # 1. Ambil data polutan & cuaca berdasarkan lokasi yang dipilih
        if location_id == "surabaya_utara":
            norm_res = get_surabaya_utara_normalisasi()
            weather_res = utara_weather.fetch_weather_utara()
        elif location_id == "surabaya_selatan":
            norm_res = get_surabaya_selatan_normalisasi()
            weather_res = selatan_weather.fetch_weather_selatan()
        elif location_id == "surabaya_timur":
            norm_res = get_surabaya_timur_normalisasi()
            weather_res = timur_weather.fetch_weather_timur()
        elif location_id == "surabaya_barat":
            norm_res = get_surabaya_barat_normalisasi()
            weather_res = barat_weather.fetch_weather_barat()
        else:  # surabaya_pusat
            norm_res = get_surabaya_pusat_normalisasi()
            weather_res = pusat_weather.fetch_weather_pusat()

        norm_data = norm_res.get_json()

        # Update polutan & catatan
        if norm_data and norm_data.get("status") == "success":
            data["pollutants"] = norm_data.get("ispu_converted", {})
            summary = norm_data.get("ispu_summary", {})
            loc_name = norm_data.get("location", "Lokasi")
            
            data["note"] = (
                f"{loc_name}: Kualitas udara saat ini berada pada kategori {summary.get('category')} "
                f"dengan Nilai ISPU Tertinggi {summary.get('max_ispu')}."
            )

        # 2. Timpa data cuaca bawaan mock_data dengan data real-time dari Open-Meteo
        if weather_res and weather_res.get("status") == "success":
            data["weather_current"] = weather_res.get("formatted", {})

        chart_series = {
            "dates": ["03 Mei", "04 Mei", "05 Mei", "06 Mei", "07 Mei", "08 Mei", "09 Mei"],
            "CO": [random.randint(5, 15) for _ in range(7)],
            "NO2": [random.randint(10, 20) for _ in range(7)],
            "O3": [random.randint(60, 80) for _ in range(7)],
            "SO2": [random.randint(70, 85) for _ in range(7)],
            "PM10": [random.randint(30, 45) for _ in range(7)],
            "PM25": [random.randint(80, 105) for _ in range(7)],
        }

        return jsonify({"status": "success", "details": data, "chart_data": chart_series})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500