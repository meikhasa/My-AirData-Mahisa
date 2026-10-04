import random
from flask import Blueprint, jsonify, render_template
from controllers.controller_view.dashboard_controller import load_mock_data
from routes.surabaya_pusat_routes.pusat_routes import get_surabaya_pusat_normalisasi
from routes.surabaya_utara_routes.utara_routes import get_surabaya_utara_normalisasi
from routes.surabaya_selatan_routes.selatan_routes import get_surabaya_selatan_normalisasi
from routes.surabaya_timur_routes.timur_routes import get_surabaya_timur_normalisasi
from routes.surabaya_barat_routes.barat_routes import get_surabaya_barat_normalisasi

from controllers.surabaya_pusat_controller.pusat_openmateo_controller import weather_openmateo

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

        # 2. Ambil data cuaca
        # weather_res = weather_openmateo.fetch_weather_pusat()
        # weather_data = weather_res.get("formatted", {}) if weather_res.get("status") == "success" else {}

        # 3. Render template dengan menyertakan air_data dan weather_data
        # return render_template("index.html", air=air_data, weather=weather_data)
    
        return render_template("index.html", air=air_data, air_quality=air_data)
    except Exception as e:
        return render_template("index.html", air={}, air_quality={})
    

@view_bp.route("/api/dashboard/<location_id>", methods=["GET"])
def get_dashboard_data(location_id):
    try:
        mock_data = load_mock_data()
        data = mock_data.get(location_id, mock_data.get("surabaya_pusat"))

        if location_id == "surabaya_utara":
            norm_res = get_surabaya_utara_normalisasi()
        elif location_id == "surabaya_selatan":
            norm_res = get_surabaya_selatan_normalisasi()
        elif location_id == "surabaya_timur":
            norm_res = get_surabaya_timur_normalisasi()
        elif location_id == "surabaya_barat":
            norm_res = get_surabaya_barat_normalisasi()
        else:
            norm_res = get_surabaya_pusat_normalisasi()

        norm_data = norm_res.get_json()

        if norm_data and norm_data.get("status") == "success":
            data["pollutants"] = norm_data.get("ispu_converted", {})
            summary = norm_data.get("ispu_summary", {})
            loc_name = norm_data.get("location", "Lokasi")
            
            data["note"] = (
                f"{loc_name}: Kualitas udara saat ini berada pada kategori {summary.get('category')} "
                f"dengan Nilai ISPU Tertinggi {summary.get('max_ispu')}."
            )

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