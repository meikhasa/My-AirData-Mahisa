import json
from datetime import datetime
from flask import jsonify
from controllers.controller_view.ispu_converter import ISPUConverter

def load_mock_data():
    with open("mock_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_normalized_data(controller_class, location_name):
    try:
        raw_data = controller_class.fetch_data_openmateo()
        hourly = raw_data.get("hourly", {})
        times = hourly.get("time", [])

        if not times:
            return jsonify({"success": False, "message": "Data Open-Meteo kosong"}), 400

        now_str = datetime.now().strftime("%Y-%m-%dT%H:00")
        current_idx = times.index(now_str) if now_str in times else 0

        raw_pollutants = {
            "CO": hourly.get("carbon_monoxide", [])[current_idx],
            "NO2": hourly.get("nitrogen_dioxide", [])[current_idx],
            "PM25": hourly.get("pm2_5", [])[current_idx],
            "PM10": hourly.get("pm10", [])[current_idx],
            "O3": hourly.get("ozone", [])[current_idx],
            "SO2": hourly.get("sulphur_dioxide", [])[current_idx],
        }

        ispu_pollutants = {
            p_name: ISPUConverter.calculate_ispu(p_name, val)
            for p_name, val in raw_pollutants.items()
        }

        valid_ispu_vals = [v for v in ispu_pollutants.values() if v is not None]
        max_ispu = max(valid_ispu_vals) if valid_ispu_vals else 0
        status_ispu = ISPUConverter.get_category(max_ispu)

        return jsonify({
            "status": "success",
            "location": location_name,
            "time_at": times[current_idx],
            "raw_data_ugm3": raw_pollutants,
            "ispu_converted": ispu_pollutants,
            "ispu_summary": {
                "max_ispu": max_ispu,
                "category": status_ispu
            },
            "header_kanan": {
                "cuaca" : "cerah",
                "angin" : "25km",
                "suhu" : "30"
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500