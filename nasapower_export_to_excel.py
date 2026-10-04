# import os
# import pandas as pd
# from flask import Flask

# # Import 5 Controller NASA Power milikmu
# from controllers.barat_nasapower_controller import column_nasapower as barat_ctrl
# from controllers.pusat_nasapower_controller import column_nasapower as pusat_ctrl
# from controllers.selatan_nasapower_controller import column_nasapower as selatan_ctrl
# from controllers.timur_nasapower_controller import column_nasapower as timur_ctrl
# from controllers.utara_nasapower_controller import column_nasapower as utara_ctrl

# # Inisialisasi app con    text Flask sederhana agar jsonify() bekerja tanpa error
# app = Flask(__name__)


# def process_and_save_nasa(controller, location_name, filename):
#     print(f"Sedang mengambil data NASA POWER untuk {location_name}...")

#     with app.app_context():
#         # Memanggil controller
#         res_tuple = controller.fetch_data_nasapower()

#         # Handle jika return berupa tuple (jsonify_response, status_code)
#         if isinstance(res_tuple, tuple):
#             response_obj = res_tuple[0]
#         else:
#             response_obj = res_tuple

#         response_json = response_obj.get_json()

#         if response_json.get("status") == "success":
#             raw_data = response_json["data"]["properties"]["parameter"]

#             # Convert JSON nested ke DataFrame
#             df = pd.DataFrame(raw_data)
#             df.index.name = "datetime_str"
#             df = df.reset_index()

#             # Format datetime dari YYYYMMDDHH
#             df["datetime"] = pd.to_datetime(df["datetime_str"], format="%Y%m%d%H")

#             # Pilih dan susun ulang kolom
#             df = df[["datetime", "T2M", "PRECTOTCORR", "WS2M", "QV2M"]]
#             df.columns = [
#                 "Datetime",
#                 "Suhu_T2M",
#                 "CurahHujan_PRECTOTCORR",
#                 "KecepatanAngin_WS2M",
#                 "Kelembapan_QV2M",
#             ]

#             # Simpan ke Excel
#             df.to_excel(filename, index=False, engine="openpyxl")
#             print(f"✅ Berhasil! File tersimpan di: {filename}\n")
#         else:
#             print(f"❌ Gagal mengambil data untuk {location_name}\n")


# if __name__ == "__main__":
#     # Buat folder khusus output agar root directory tetap rapi
#     output_dir = "dataset_nasa_excel"
#     os.makedirs(output_dir, exist_ok=True)

#     # Daftar wilayah yang akan diproses
#     targets = [
#         (pusat_ctrl, "Surabaya Pusat", f"{output_dir}/nasa_surabaya_pusat.xlsx"),
#         (utara_ctrl, "Surabaya Utara", f"{output_dir}/nasa_surabaya_utara.xlsx"),
#         (selatan_ctrl, "Surabaya Selatan", f"{output_dir}/nasa_surabaya_selatan.xlsx"),
#         (timur_ctrl, "Surabaya Timur", f"{output_dir}/nasa_surabaya_timur.xlsx"),
#         (barat_ctrl, "Surabaya Barat", f"{output_dir}/nasa_surabaya_barat.xlsx"),
#     ]

#     for ctrl, loc, path in targets:
#         process_and_save_nasa(ctrl, loc, path)

#     print("=== PROSES SELESAI! SEMUA FILE EXCEL TELAH DIBUAT ===")