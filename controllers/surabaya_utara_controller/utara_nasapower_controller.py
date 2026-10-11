# import requests
# from flask import jsonify

# class column_nasapower:
    
#     @staticmethod
#     def fetch_data_nasapower():
#         url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        
#         # Menggunakan tanggal sesuai permintaan: 20200101 s/d 20251231
#         params = {
#             "parameters": "T2M,PRECTOTCORR,WS2M,QV2M",
#             "community": "RE",
#             "latitude": -7.2100,
#             "longitude": 112.7300,
#             "start": "20200101",
#             "end": "20251231",
#             "format": "JSON"
#         }
        
#         try:
#             response = requests.get(url, params=params, timeout=30)
#             response.raise_for_status()
            
#             data = response.json()
#             print("Berhasil mengambil data dari NASA POWER API\n")
            
#             return jsonify({
#                 "status": "success",
#                 "location": "Surabaya Utara",
#                 "parameters_fetched": ["T2M", "PRECTOTCORR", "WS2M", "QV2M"],
#                 "data": data
#             }), 200

#         except requests.exceptions.RequestException as e:
#             print(f"Gagal mengambil data NASA POWER. Error: {e}")
#             return jsonify({
#                 "status": "error",
#                 "message": f"Gagal mengambil data dari NASA POWER: {str(e)}"
#             }), 500

import requests
from flask import jsonify

class column_nasapower:
    
    @staticmethod
    def fetch_data_nasapower():
        url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        
        # REVISI: Mengubah parameter PRECTOTCORR -> PRECTOT dan community RE -> AG
        params = {
            "parameters": "T2M,PRECTOT,WS2M,QV2M",
            "community": "AG",
            "latitude": -7.2100,   
            "longitude": 112.7300,
            "start": "20200101",
            "end": "20251231",
            "format": "JSON"
        }
        
        try:
            # Timeout diperbesar sedikit (60 detik) karena data 6 tahun cukup berat
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            print("Berhasil mengambil data dari NASA POWER API\n")
            
            return jsonify({
                "status": "success",
                "location": "Surabaya Utara", 
                "parameters_fetched": ["T2M", "PRECTOT", "WS2M", "QV2M"],
                "data": data
            }), 200

        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil data NASA POWER. Error: {e}")
            return jsonify({
                "status": "error",
                "message": f"Gagal mengambil data dari NASA POWER: {str(e)}"
            }), 500