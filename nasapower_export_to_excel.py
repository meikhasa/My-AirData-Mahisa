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

import os
import pandas as pd
import numpy as np
from flask import Flask

# Import 5 Controller NASA Power sesuai struktur folder VS Code
from controllers.surabaya_barat_controller.barat_nasapower_controller import column_nasapower as barat_ctrl
from controllers.surabaya_pusat_controller.pusat_nasapower_controller import column_nasapower as pusat_ctrl
from controllers.surabaya_selatan_controller.selatan_nasapower_controller import column_nasapower as selatan_ctrl
from controllers.surabaya_timur_controller.timur_nasapower_controller import column_nasapower as timur_ctrl
from controllers.surabaya_utara_controller.utara_nasapower_controller import column_nasapower as utara_ctrl

app = Flask(__name__)

def process_and_save_nasa(controller, location_name, filename):
    print(f"Sedang mengambil data NASA POWER untuk {location_name}...")

    with app.app_context():
        # Memanggil controller
        res_tuple = controller.fetch_data_nasapower()

        if isinstance(res_tuple, tuple):
            response_obj = res_tuple[0]
        else:
            response_obj = res_tuple

        response_json = response_obj.get_json()

        if response_json.get("status") == "success":
            raw_data = response_json["data"]["properties"]["parameter"]

            # Convert JSON nested ke DataFrame
            df = pd.DataFrame(raw_data)
            df.index.name = "datetime_str"
            df = df.reset_index()

            # Format datetime dari YYYYMMDDHH
            df["datetime"] = pd.to_datetime(df["datetime_str"], format="%Y%m%d%H")

            # DETEKSI OTOMATIS: Cari kolom curah hujan (baik PRECTOTCORR maupun PRECTOT)
            precip_col = "PRECTOTCORR" if "PRECTOTCORR" in df.columns else ("PRECTOT" if "PRECTOT" in df.columns else None)
            
            # Susun daftar kolom yang akan diproses
            cols_to_select = ["datetime", "T2M"]
            if precip_col:
                cols_to_select.append(precip_col)
            cols_to_select.extend(["WS2M", "QV2M"])

            df = df[cols_to_select]

            # Rename nama kolom ke format standar
            rename_dict = {
                "datetime": "Datetime",
                "T2M": "Suhu_T2M",
                "WS2M": "KecepatanAngin_WS2M",
                "QV2M": "Kelembapan_QV2M"
            }
            if precip_col:
                rename_dict[precip_col] = "CurahHujan_PRECTOTCORR"

            df = df.rename(columns=rename_dict)

            # =========================================================================
            # PEMBERSIHAN DATA (CLEANSING)
            # 1. Curah hujan: Ubah semua nilai negatif (-999, -98979.2, dll) menjadi 0.0
            # 2. Suhu, Angin, Kelembapan: Isi data kosong dengan penanganan ffill/bfill
            # =========================================================================
            if "CurahHujan_PRECTOTCORR" in df.columns:
                df["CurahHujan_PRECTOTCORR"] = df["CurahHujan_PRECTOTCORR"].apply(
                    lambda x: x if (pd.notna(x) and x >= 0) else 0.0
                )

            for col in ["Suhu_T2M", "KecepatanAngin_WS2M", "Kelembapan_QV2M"]:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: np.nan if (pd.isna(x) or x < -100) else x)
                    df[col] = df[col].ffill().bfill()

            # Simpan ke CSV
            df.to_csv(filename, index=False)
            print(f"✅ Berhasil! File tersimpan di: {filename}\n")
        else:
            print(f"❌ Gagal mengambil data untuk {location_name}\n")

if __name__ == "__main__":
    output_dir = "dataset_nasa_csv"
    os.makedirs(output_dir, exist_ok=True)

    targets = [
        (pusat_ctrl, "Surabaya Pusat", f"{output_dir}/nasa_surabaya_pusat.csv"),
        (utara_ctrl, "Surabaya Utara", f"{output_dir}/nasa_surabaya_utara.csv"),
        (selatan_ctrl, "Surabaya Selatan", f"{output_dir}/nasa_surabaya_selatan.csv"),
        (timur_ctrl, "Surabaya Timur", f"{output_dir}/nasa_surabaya_timur.csv"),
        (barat_ctrl, "Surabaya Barat", f"{output_dir}/nasa_surabaya_barat.csv"),
    ]

    for ctrl, loc, path in targets:
        process_and_save_nasa(ctrl, loc, path)

    print("=== PROSES SELESAI! SEMUA FILE CSV TELAH DIBUAT ===")