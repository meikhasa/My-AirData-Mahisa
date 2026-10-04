# import json
# import random
# from datetime import datetime
# from flask import Blueprint, jsonify, render_template

# # ==========================================
# # 1. IMPORT OPEN-METEO CONTROLLERS (5 WILAYAH)
# # ==========================================
# from controllers.surabaya_pusat_controller.pusat_openmateo_controller import pollutant_openmateo as pusat_ctrl
# from controllers.surabaya_utara_controller.utara_openmateo_controller import pollutant_openmateo as utara_ctrl
# from controllers.surabaya_selatan_controller.selatan_openmateo_controller import pollutant_openmateo as selatan_ctrl
# from controllers.surabaya_timur_controller.timur_openmateo_controller import pollutant_openmateo as timur_ctrl
# from controllers.surabaya_barat_controller.barat_openmateo_controller import pollutant_openmateo as barat_ctrl

# # ==========================================
# # 2. IMPORT NASA POWER CONTROLLERS (5 WILAYAH)
# # ==========================================
# from controllers.surabaya_pusat_controller.pusat_nasapower_controller import column_nasapower as pusat_nasa_ctrl
# from controllers.surabaya_utara_controller.utara_nasapower_controller import column_nasapower as utara_nasa_ctrl
# from controllers.surabaya_selatan_controller.selatan_nasapower_controller import column_nasapower as selatan_nasa_ctrl
# from controllers.surabaya_timur_controller.timur_nasapower_controller import column_nasapower as timur_nasa_ctrl
# from controllers.surabaya_barat_controller.barat_nasapower_controller import column_nasapower as barat_nasa_ctrl

# from controllers.controller_view.ispu_converter import ISPUConverter

# from controllers.surabaya_pusat_controller.pusat_openmateo_controller import weather_openmateo

# # Inisialisasi Blueprint
# api_bp_web = Blueprint("dashboard", __name__)


# def load_mock_data():
#     with open("mock_data.json", "r", encoding="utf-8") as f:
#         return json.load(f)


# # HELPER FUNCTION: Biar kodenya efisien dan tidak diulang-ulang 5 kali
# def get_normalized_data(controller_class, location_name):
#     try:
#         raw_data = controller_class.fetch_data_openmateo()
#         hourly = raw_data.get("hourly", {})
#         times = hourly.get("time", [])

#         if not times:
#             return jsonify({"success": False, "message": "Data Open-Meteo kosong"}), 400

#         now_str = datetime.now().strftime("%Y-%m-%dT%H:00")
#         current_idx = times.index(now_str) if now_str in times else 0

#         raw_pollutants = {
#             "CO": hourly.get("carbon_monoxide", [])[current_idx],
#             "NO2": hourly.get("nitrogen_dioxide", [])[current_idx],
#             "PM25": hourly.get("pm2_5", [])[current_idx],
#             "PM10": hourly.get("pm10", [])[current_idx],
#             "O3": hourly.get("ozone", [])[current_idx],
#             "SO2": hourly.get("sulphur_dioxide", [])[current_idx],
#         }

#         ispu_pollutants = {
#             p_name: ISPUConverter.calculate_ispu(p_name, val)
#             for p_name, val in raw_pollutants.items()
#         }

#         valid_ispu_vals = [v for v in ispu_pollutants.values() if v is not None]
#         max_ispu = max(valid_ispu_vals) if valid_ispu_vals else 0
#         status_ispu = ISPUConverter.get_category(max_ispu)

#         return jsonify({
#             "status": "success",
#             "location": location_name,
#             "time_at": times[current_idx],
#             "raw_data_ugm3": raw_pollutants,
#             "ispu_converted": ispu_pollutants,
#             "ispu_summary": {
#                 "max_ispu": max_ispu,
#                 "category": status_ispu
#             }
#         })

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# # ==========================================
# # 1. HALAMAN UTAMA WEB
# # ==========================================
# @api_bp_web.route("/")
# def index():
#     try:
#         res = get_surabaya_pusat_normalisasi()
#         norm_data = res.get_json()

#         if norm_data and norm_data.get("status") == "success":
#             converted = norm_data.get("ispu_converted", {})
#             air_data = {
#                 "co": converted.get("CO"),
#                 "no2": converted.get("NO2"),
#                 "pm25": converted.get("PM25"),
#                 "pm10": converted.get("PM10"),
#                 "o3": converted.get("O3"),
#                 "so2": converted.get("SO2"),
#             }
#         else:
#             air_data = {}

#         return render_template("index.html", air=air_data, air_quality=air_data)
#     except Exception as e:
#         return render_template("index.html", air={}, air_quality={})

# # ==========================================
# # ENDPOINT WEATHER SURABAYA PUSAT
# # ==========================================
# @api_bp_web.route("/surabaya_pusat_weather")
# def get_surabaya_pusat_weather():
#     res = weather_openmateo.fetch_weather_pusat()
#     return jsonify(res)

# # ==========================================
# # 2. ENDPOINT NORMALISASI OPEN-METEO (5 WILAYAH)
# # ==========================================
# @api_bp_web.route("/surabaya_pusat_normalisasi")
# def get_surabaya_pusat_normalisasi():
#     return get_normalized_data(pusat_ctrl, "Surabaya Pusat")

# @api_bp_web.route("/surabaya_utara_normalisasi")
# def get_surabaya_utara_normalisasi():
#     return get_normalized_data(utara_ctrl, "Surabaya Utara")

# @api_bp_web.route("/surabaya_selatan_normalisasi")
# def get_surabaya_selatan_normalisasi():
#     return get_normalized_data(selatan_ctrl, "Surabaya Selatan")

# @api_bp_web.route("/surabaya_timur_normalisasi")
# def get_surabaya_timur_normalisasi():
#     return get_normalized_data(timur_ctrl, "Surabaya Timur")

# @api_bp_web.route("/surabaya_barat_normalisasi")
# def get_surabaya_barat_normalisasi():
#     return get_normalized_data(barat_ctrl, "Surabaya Barat")


# # ==========================================
# # 3. ENDPOINT NASA POWER (5 WILAYAH)
# # ==========================================
# @api_bp_web.route("/surabaya_pusat_nasa")
# def get_surabaya_pusat_nasa():
#     return pusat_nasa_ctrl.fetch_data_nasapower()

# @api_bp_web.route("/surabaya_utara_nasa")
# def get_surabaya_utara_nasa():
#     return utara_nasa_ctrl.fetch_data_nasapower()

# @api_bp_web.route("/surabaya_selatan_nasa")
# def get_surabaya_selatan_nasa():
#     return selatan_nasa_ctrl.fetch_data_nasapower()

# @api_bp_web.route("/surabaya_timur_nasa")
# def get_surabaya_timur_nasa():
#     return timur_nasa_ctrl.fetch_data_nasapower()

# @api_bp_web.route("/surabaya_barat_nasa")
# def get_surabaya_barat_nasa():
#     return barat_nasa_ctrl.fetch_data_nasapower()


# # ==========================================
# # 4. ENDPOINT DASHBOARD (DENGAN ROUTING INTEGRASI)
# # ==========================================
# @api_bp_web.route("/api/dashboard/<location_id>", methods=["GET"])
# def get_dashboard_data(location_id):
#     try:
#         mock_data = load_mock_data()
#         data = mock_data.get(location_id, mock_data.get("surabaya_pusat"))

#         # Pilih endpoint berdasarkan location_id
#         if location_id == "surabaya_utara":
#             norm_res = get_surabaya_utara_normalisasi()
#         elif location_id == "surabaya_selatan":
#             norm_res = get_surabaya_selatan_normalisasi()
#         elif location_id == "surabaya_timur":
#             norm_res = get_surabaya_timur_normalisasi()
#         elif location_id == "surabaya_barat":
#             norm_res = get_surabaya_barat_normalisasi()
#         else:
#             norm_res = get_surabaya_pusat_normalisasi()

#         norm_data = norm_res.get_json()

#         if norm_data and norm_data.get("status") == "success":
#             data["pollutants"] = norm_data.get("ispu_converted", {})
#             summary = norm_data.get("ispu_summary", {})
#             loc_name = norm_data.get("location", "Lokasi")
            
#             data["note"] = (
#                 f"{loc_name}: Kualitas udara saat ini berada pada kategori {summary.get('category')} "
#                 f"dengan Nilai ISPU Tertinggi {summary.get('max_ispu')}."
#             )

#         chart_series = {
#             "dates": ["03 Mei", "04 Mei", "05 Mei", "06 Mei", "07 Mei", "08 Mei", "09 Mei"],
#             "CO": [random.randint(5, 15) for _ in range(7)],
#             "NO2": [random.randint(10, 20) for _ in range(7)],
#             "O3": [random.randint(60, 80) for _ in range(7)],
#             "SO2": [random.randint(70, 85) for _ in range(7)],
#             "PM10": [random.randint(30, 45) for _ in range(7)],
#             "PM25": [random.randint(80, 105) for _ in range(7)],
#         }

#         return jsonify({"status": "success", "details": data, "chart_data": chart_series})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500